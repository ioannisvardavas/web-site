const http = require("http");
const fs = require("fs");
const path = require("path");

const ROOT = path.resolve(__dirname, "..");
// Το Ραντάρ Ρίσκου (ξεχωριστό repo, δίπλα) σερβίρεται κάτω από /risk-radar/,
// ώστε η δοκιμαστική σελίδα να ανοίγει την τοπική, νέα του μορφή.
const RADAR = path.resolve(__dirname, "..", "..", "risk-radar");
const PORT = process.env.PORT || 8899;
const TYPES = { ".html": "text/html", ".png": "image/png", ".jpg": "image/jpeg",
  ".css": "text/css", ".js": "text/javascript", ".svg": "image/svg+xml",
  ".json": "application/json", ".webp": "image/webp", ".woff2": "font/woff2", ".ico": "image/x-icon" };

http.createServer((req, res) => {
  let rel = decodeURIComponent(req.url.split("?")[0]);
  if (rel === "/") rel = "/standalone.html";
  else if (rel.endsWith("/")) rel += "index.html";
  if (rel === "/risk-radar") { res.writeHead(301, { Location: "/risk-radar/" }); return res.end(); }
  const base = rel.startsWith("/risk-radar/") ? RADAR : ROOT;
  if (base === RADAR) rel = rel.slice("/risk-radar".length);
  const file = path.join(base, rel);
  if (!file.startsWith(base)) { res.writeHead(403); return res.end(); }
  fs.readFile(file, (err, data) => {
    if (err) { res.writeHead(404); return res.end("not found"); }
    res.writeHead(200, { "Content-Type": TYPES[path.extname(file)] || "application/octet-stream" });
    // Τοπικά, το «← Στην ιστοσελίδα μου» του ραντάρ γυρνά στη δοκιμαστική σελίδα, όχι στο ζωντανό site.
    if (base === RADAR && path.extname(file) === ".html")
      data = data.toString().split("https://vardavas-site.pages.dev").join("/standalone_v4.html");
    res.end(data);
  });
}).listen(PORT, () => console.log("listening on " + PORT));
