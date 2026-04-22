import base64
import os

def inject_base64():
    path = "/Users/cp/Ronak/CP/HR/RnR/"
    html_file = os.path.join(path, "certificate-generator.html")
    
    with open(html_file, 'r') as f:
        content = f.read()
    
    # Read Base64 files
    with open(os.path.join(path, "Images/CP-2.base64"), 'r') as f:
        cp_b64 = f.read().strip()
    
    with open(os.path.join(path, "Images/WF247-2.base64"), 'r') as f:
        wf_b64 = f.read().strip()
        
    # Replace the image loading logic
    old_code = """        // Load images
        images.CP.src = 'Images/CP-2.png';
        images.WF247.src = 'Images/WF247-2.png';"""
        
    new_code = f"""        // Load images as Base64 to bypass browser security (no server needed)
        images.CP.src = 'data:image/png;base64,{cp_b64}';
        images.WF247.src = 'data:image/png;base64,{wf_b64}';"""
        
    content = content.replace(old_code, new_code)
    
    with open(html_file, 'w') as f:
        f.write(content)
    
    print("Injected Base64 successfully.")

if __name__ == "__main__":
    inject_base64()
