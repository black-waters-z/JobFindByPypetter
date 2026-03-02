const { app, BrowserWindow } = require("electron");
const { spawn } = require("child_process");
const path = require("path");

let mainWindow;
let pythonProcess;
const isDev = !app.isPackaged;

function getBackendCommand() {
  if (isDev) {
    return { cmd: "python", args: ["../backend/main.py"] };
  }
  const exePath = path.join(process.resourcesPath, "backend", "backend.exe");
  return { cmd: exePath, args: [] };
}

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 900,
    height: 700,
    resizable: false,
    maximizable: false,
    autoHideMenuBar: true,
    webPreferences: {
      preload: path.join(__dirname, "preload.js"),
    },
  });

  if (isDev) {
    mainWindow.loadURL("http://localhost:5173");
  } else {
    mainWindow.loadFile(path.join(__dirname, "dist/renderer/index.html"));
  }

  if (isDev) {
    mainWindow.webContents.openDevTools();
  }
}

app.whenReady().then(() => {
  const { cmd, args } = getBackendCommand();
  const env = { ...process.env };
  if (!isDev) {
    const portableDir =
      process.env.PORTABLE_EXECUTABLE_DIR || path.dirname(app.getPath("exe"));
    env.CONFIG_PATH = path.join(portableDir, "config.json");
  }
  pythonProcess = spawn(cmd, args, { stdio: "ignore", env });
  createWindow();
});

app.on("will-quit", () => {
  if (pythonProcess && !pythonProcess.killed) {
    pythonProcess.kill();
  }
});
