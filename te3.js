import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";
import { JSDOM } from "jsdom";

// Get the current directory
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Define directories
const htmlDir = path.join(__dirname, "html2");
const csvDir = path.join(__dirname, "csv");

// Ensure output directory exists
if (!fs.existsSync(csvDir)) {
    fs.mkdirSync(csvDir, { recursive: true });
}

// Function to extract and format data from HTML
function extractDataFromHTML(html) {
    const dom = new JSDOM(html);
    const document = dom.window.document;
    const rows = [];

    document.querySelectorAll("p").forEach(p => {
        let text = p.textContent.trim();
        if (!text) return;

        // Replace any 3 to 12 spaces with ';'
        let formattedRow = text.replace(/ {3,12}/g, ";");

        // Remove commas and replace with space
        formattedRow = formattedRow.replace(/,/g, " ");

        rows.push(formattedRow);
    });

    return rows;
}

// Function to process all HTML files in html2/
function processHTMLFiles() {
    fs.readdir(htmlDir, (err, files) => {
        if (err) {
            console.error("❌ Error reading HTML directory:", err);
            return;
        }

        files.forEach(file => {
            if (file.endsWith(".html")) {
                const filePath = path.join(htmlDir, file);
                const outputCSVPath = path.join(csvDir, file.replace(".html", ".csv"));

                fs.readFile(filePath, "utf8", (err, html) => {
                    if (err) {
                        console.error(`❌ Error reading ${file}:`, err);
                        return;
                    }

                    const data = extractDataFromHTML(html);
                    if (data.length > 0) {
                        const csvContent = data.join("\n");
                        fs.writeFileSync(outputCSVPath, csvContent);
                        console.log(`✅ Converted: ${file} → ${outputCSVPath}`);
                    } else {
                        console.warn(`⚠️ No transactions found in ${file}`);
                    }
                });
            }
        });
    });
}

// Run the script
processHTMLFiles();
