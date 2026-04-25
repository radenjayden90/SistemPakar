document.getElementById("diagnosaForm").addEventListener("submit", async function(e){
    e.preventDefault();

    const checkboxes = document.querySelectorAll('input[name="gejala"]:checked');
    const gejalaInputs = Array.from(checkboxes).map(cb => cb.value);

    // Elements
    const btnText = document.querySelector(".btn-text");
    const loader = document.querySelector(".loader");
    const submitBtn = document.getElementById("submitBtn");
    const hasilBox = document.getElementById("hasilBox");
    const resultContent = document.getElementById("resultContent");
    
    // UI Loading State
    btnText.style.display = "none";
    loader.style.display = "block";
    submitBtn.disabled = true;

    try {
        const res = await fetch("http://localhost:5001/diagnosa", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({gejala: gejalaInputs})
        });

        if (!res.ok) throw new Error("Gagal menghubungi server pakar");
        
        const data = await res.json();
        
        // Hide Loader
        btnText.style.display = "block";
        loader.style.display = "none";
        submitBtn.disabled = false;

        // Render hasil
        hasilBox.classList.remove("hidden");
        
        if (data.status === "success") {
            resultContent.innerHTML = `
                <p>Status: <span style="color:var(--neon-green)">DITEMUKAN</span></p>
                <span class="penyakit-highlight">[${data.penyakit}]</span>
                <p style="margin-top:10px; color:#ccc;"><strong>Rekomendasi Penanganan:</strong><br> ${data.solusi}</p>
            `;
        } else {
            resultContent.innerHTML = `
                <p>Status: <span style="color:orange">UNKNOWN_ERROR</span></p>
                <p style="color:#ccc; margin-top:10px;">${data.pesan}</p>
            `;
        }
        
    } catch (error) {
        alert("Eror: " + error.message);
        btnText.style.display = "block";
        loader.style.display = "none";
        submitBtn.disabled = false;
    }
});
