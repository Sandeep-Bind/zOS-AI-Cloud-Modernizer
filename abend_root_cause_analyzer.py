import os
import re
from datetime import datetime

class GenAIAbendTriageAgent:
    """
    Simulates an intelligent GenAI-powered GOC monitoring daemon 
    that analyzes mainframe spool output and provides automated remediation.
    """
    def __init__(self, spool_log_content):
        self.log_content = spool_log_content

    def analyze_failure(self):
        print(f"[{datetime.now()}] [AI-AGENT] Analyzing mainframe spool log...")
        
        abend_match = re.search(r"SYSTEM COMPLETION CODE=([0-9A-F]+)\s+REASON CODE=([0-9A-F]+)", self.log_content)
        db2_match = re.search(r"SQLCODE=([-0-9]+)", self.log_content)
        
        diagnosis = []
        if abend_match:
            code, reason = abend_match.groups()
            diagnosis.append(self._diagnose_system_abend(code, reason))
        
        if db2_match:
            sqlcode = db2_match.group(1)
            diagnosis.append(self._diagnose_db2_error(sqlcode))
            
        return diagnosis if diagnosis else ["No critical abends detected in spool stream."]

    def _diagnose_system_abend(self, code, reason):
        kb = {
            "0C4": "Protection Exception: Invalid memory address dereference or uninitialized pointer in COBOL Linkage Section.",
            "322": "Maximum CPU time exceeded for job step. Review REGION parameter or infinite loop in batch logic.",
            "806": "Load module not found in STEPLIB concatenation. Verify library allocations."
        }
        return f"System Abend S{code} (Reason: {reason}): {kb.get(code, 'Unknown system failure.')}"

    def _diagnose_db2_error(self, sqlcode):
        if sqlcode == "-911":
            return "DB2 Deadlock or Timeout detected. Transaction rolled back. Check concurrent batch windows."
        elif sqlcode == "-803":
            return "DB2 Duplicate Key violation on insert. Primary key constraint failure."
        return f"DB2 SQLCODE {sqlcode} encountered during execution."

if __name__ == "__main__":
    sample_log = """
    IEA995I SYMPTOM DUMP OUTPUT  
    SYSTEM COMPLETION CODE=0C4  REASON CODE=00000004
    DSNQ001I - DB2P ERROR SQLCODE=-911
    """
    agent = GenAIAbendTriageAgent(sample_log)
    for report in agent.analyze_failure():
        print(f">> {report}")
