"""
IPA operations module for patching and processing iOS apps
"""
import os
import subprocess
import zipfile
import shutil
from pathlib import Path
from typing import Optional, Tuple
import logging

logger = logging.getLogger(__name__)


class IPAOperations:
    """Handle all IPA-related operations"""
    
    def __init__(self, temp_dir: str, ipapatch_bin: str, dylib_path: str):
        self.temp_dir = temp_dir
        self.ipapatch_bin = ipapatch_bin
        self.dylib_path = dylib_path
        os.makedirs(temp_dir, exist_ok=True)
    
    def patch_ipa(self, ipa_path: str, output_path: Optional[str] = None) -> Tuple[bool, str]:
        """Patch IPA with blatantsPatch.dylib using ipapatch"""
        if not os.path.exists(self.ipapatch_bin):
            return False, f"ipapatch binary not found at {self.ipapatch_bin}"
        
        if not os.path.exists(self.dylib_path):
            return False, f"Dylib not found at {self.dylib_path}"
        
        if not os.path.exists(ipa_path):
            return False, f"IPA file not found at {ipa_path}"
        
        if not output_path:
            base_name = Path(ipa_path).stem
            output_path = os.path.join(self.temp_dir, f"{base_name}_patched.ipa")
        
        try:
            # Make ipapatch executable
            os.chmod(self.ipapatch_bin, 0o755)
            
            cmd = [
                self.ipapatch_bin,
                ipa_path,
                "-o", output_path,
                "-i", self.dylib_path
            ]
            
            logger.info(f"Running ipapatch: {' '.join(cmd)}")
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=600  # 10 minutes timeout
            )
            
            if result.returncode == 0 and os.path.exists(output_path):
                logger.info(f"Successfully patched IPA: {output_path}")
                return True, output_path
            else:
                error_msg = result.stderr or result.stdout or "Unknown error"
                logger.error(f"Patching failed: {error_msg}")
                return False, f"Patching failed: {error_msg[:200]}"
                
        except subprocess.TimeoutExpired:
            logger.error("Patching timed out")
            return False, "Patching timed out (10 minutes)"
        except Exception as e:
            logger.error(f"Error during patching: {e}")
            return False, f"Error during patching: {str(e)}"
    
    def cleanup_file(self, file_path: str) -> bool:
        """Clean up a file or directory"""
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
            return True
        except Exception as e:
            logger.error(f"Error cleaning up {file_path}: {e}")
            return False
