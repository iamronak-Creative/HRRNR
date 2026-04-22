import os
import re

def fix_html():
    print("Reading Base64 files...")
    with open('Images/CP-2.base64', 'r') as f:
        cp_b64 = f.read().strip()
    with open('Images/WF247-2.base64', 'r') as f:
        wf247_b64 = f.read().strip()

    print("Reading HTML file...")
    with open('certificate-generator.html', 'r') as f:
        content = f.read()

    # Define the full script block
    new_script = f"""    <script>
        const canvas = document.getElementById('certCanvas');
        const ctx = canvas.getContext('2d');
        const loading = document.getElementById('loading');

        let currentBrand = 'CP';
        const images = {{
            CP: new Image(),
            WF247: new Image()
        }};

        let imagesLoaded = 0;
        const totalImages = 2;

        function updateLoadingStatus(msg) {{
            console.log(msg);
            const loadingDiv = document.getElementById('loading');
            if (loadingDiv) {{
                loadingDiv.innerText = msg;
            }}
        }}

        function onImageLoad(brand) {{
            imagesLoaded++;
            updateLoadingStatus(`Loaded ${{brand}} (${{imagesLoaded}}/${{totalImages}})...`);
            if (imagesLoaded === totalImages) {{
                document.getElementById('loading').style.display = 'none';
                draw();
            }}
        }}

        function onImageError(brand) {{
            console.error(`Error loading ${{brand}}`);
            document.getElementById('errorMsg').style.display = 'block';
            const loadingDiv = document.getElementById('loading');
            if (loadingDiv) {{
                loadingDiv.style.color = 'red';
                loadingDiv.innerText = `Error loading ${{brand}} template. Please refresh.`;
            }}
        }}

        // Timeout fallback
        setTimeout(() => {{
            if (imagesLoaded < totalImages) {{
                const loadingDiv = document.getElementById('loading');
                if (loadingDiv) {{
                    loadingDiv.style.color = 'orange';
                    loadingDiv.innerText = "Loading is taking longer than expected... " + (imagesLoaded) + "/" + totalImages + " loaded.";
                }}
            }}
        }}, 15000);

        images.CP.onload = () => onImageLoad('CP');
        images.CP.onerror = () => onImageError('CP');
        images.WF247.onload = () => onImageLoad('WF247');
        images.WF247.onerror = () => onImageError('WF247');

        updateLoadingStatus("Initializing templates...");
        images.CP.src = 'data:image/png;base64,{cp_b64}';
        images.WF247.src = 'data:image/png;base64,{wf247_b64}';

        function setBrand(brand) {{
            currentBrand = brand;
            // Update active state in UI
            document.querySelectorAll('.brand-btn').forEach(btn => {{
                btn.classList.toggle('active', btn.innerText.includes(brand));
            }});
            draw();
        }}

        function draw() {{
            if (imagesLoaded < totalImages) return;

            const name = (document.getElementById("userName").value || "RECIPIENT NAME").toUpperCase();
            const dept = document.getElementById('userDept').value || "DEPARTMENT NAME";
            const date = document.getElementById('certDate').value || "";
            const offX = 0;
            const offY = 0;

            ctx.clearRect(0, 0, canvas.width, canvas.height);
            ctx.drawImage(images[currentBrand], 0, 0);

            ctx.fillStyle = "black";
            ctx.textAlign = "center";

            if (currentBrand === 'WF247') {{
                const ptScale = 4.16;
                const centerX = 2700;

                // Name: Playfair Display (Italic Bold) - Elegant Navy Blue
                ctx.font = `italic 700 ${{46 * ptScale}}px "Playfair Display", serif`;
                ctx.fillStyle = '#1D3557';
                ctx.fillText(name, centerX + offX, 1800 + offY);

                // Dept: Montserrat (Regular)
                ctx.font = `400 ${{20 * ptScale}}px "Montserrat", sans-serif`;
                ctx.fillStyle = '#111111';
                ctx.fillText(dept, centerX + offX, 1920 + offY);

                // Date: Positioned above the DATE label on the line
                if (date) {{
                    ctx.textAlign = 'left';
                    ctx.font = `400 ${{14 * ptScale}}px "Montserrat", sans-serif`;
                    ctx.fillStyle = '#111111';
                    ctx.fillText(date, 1950, 2650);
                }}
            }} else {{
                const ptScale = 4.16;
                const centerX = 3200;

                // Name: Bold black serif
                ctx.font = `700 ${{40 * ptScale}}px "Lora", serif`;
                ctx.fillStyle = '#000000';
                ctx.fillText(name, centerX + offX, 1300 + offY);

                // Dept: Montserrat Regular
                ctx.font = `400 ${{18 * ptScale}}px "Montserrat", sans-serif`;
                ctx.fillStyle = '#000000';
                ctx.fillText(dept, centerX + offX, 1430 + offY);

                // Date: Positioned above the DATE label on the line
                if (date) {{
                    ctx.textAlign = 'center';
                    ctx.font = `600 ${{14 * ptScale}}px "Montserrat", sans-serif`;
                    ctx.fillStyle = '#333333';
                    ctx.fillText(date, 2800, 2560);
                }}
            }}
        }}

        function download() {{
            try {{
                const name = document.getElementById('userName').value || "Certificate";
                canvas.toBlob((blob) => {{
                    if (!blob) {{
                        document.getElementById('errorMsg').style.display = 'block';
                        return;
                    }}
                    const link = document.createElement('a');
                    link.download = `${{currentBrand}}_Certificate_${{name.replace(/\\s+/g, '_')}}.jpg`;
                    link.href = URL.createObjectURL(blob);
                    link.click();
                    setTimeout(() => URL.revokeObjectURL(link.href), 10000);
                }}, 'image/jpeg', 0.95);
            }} catch (e) {{
                console.error(e);
                document.getElementById('errorMsg').style.display = 'block';
            }}
        }}

        document.getElementById("certDate").value = new Date().toLocaleDateString("en-GB");
        document.fonts.ready.then(() => {{
            draw();
        }});
    </script>"""

    print("Injecting script block...")
    # Match the entire script block and replace it
    # We use a non-greedy match to find the FIRST script tag (the main one)
    # The HTML only has one main script tag at the bottom.
    script_pattern = r'<script>.*?</script>'
    new_content = re.sub(script_pattern, lambda m: new_script, content, flags=re.DOTALL)

    print("Writing updated HTML...")
    with open('certificate-generator.html', 'w') as f:
        f.write(new_content)
    print("Done.")

if __name__ == "__main__":
    fix_html()
