import json
import subprocess

from domain.values.contract import ProgramID


class SolanaDeployer:
    def deploy(self, code: str) -> ProgramID:
        subprocess.run(["anchor", "build"], check=True)
        
        with open("target/idl/program.json") as f:
            program_id = json.load(f)["metadata"]["address"]
        
        updated_code = code.replace("TEMP_PROGRAM_ID", program_id)
        return ProgramID(program_id), updated_code