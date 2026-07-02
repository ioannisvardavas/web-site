const http = require("http");
const fs = require("fs");
const path = require("path");

const ROOT = "/Users/user/Desktop/Claude dir/ΕΠΕΝΔΥΩ ΓΙΑ ΤΟ ΜΕΛΛΟΝ/mobile_deploy";
const PORT = 8099;
const TYPES = { ".html": "text/html", ".png": "image/png", ".jpg": "image/jpeg",
  ".css": "text/css", ".js": "text/javascript", ".svg": "image/svg+xml" };

http.createServer((req, res) => {
  let rel = decodeURIComponent(req.url.split("?")[0]);
  if (rel === "/") rel = "/index.html";
  const file = path.join(ROOT, rel);
  if (!file.startsWith(ROOT)) { res.writeHead(403); return res.end(); }
  fs.readFile(file, (err, data) => {
    if (err) { res.writeHead(404); return res.end("not found"); }
    res.writeHead(200, { "Content-Type": TYPES[path.extname(file)] || "application/octet-stream" });
    res.end(data);
  });
}).listen(PORT, () => console.log("listening on " + PORT));
