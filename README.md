# Card & Booklet Generator

Installable on **phone and computer**. Design report cards, due cards and record booklets, then print them on A4. After install it runs in its own window and works **offline**.

## Install on a computer (Windows, Mac, Linux)

1. Open the app in **Chrome** or **Microsoft Edge**.
2. Click **Install app** on the page, or the install icon in the address bar.
3. Due Books opens in its own window, like any other desktop program.
4. Pin it to the taskbar or the Dock.

## Install on a phone

### Android
1. Open the app in **Chrome**.
2. Tap **Install** (or Chrome menu → **Install app** / **Add to Home screen**).
3. Open **Due Books** from your home screen.

### iPhone / iPad
1. Open the app in **Safari** (not Chrome).
2. Tap the **Share** button (square with an arrow).
3. Tap **Add to Home Screen**, then **Add**.
4. Open **Due Books** from your home screen.

## Run it on this computer (needed once, to install)

The app must be opened over `http://` (not as a file) so the phone and computer can install it.

```bash
python3 serve.py
```

Then:

- On this computer: [http://127.0.0.1:8080](http://127.0.0.1:8080)
- On a phone on the same Wi‑Fi: use the `http://YOUR-LAN-IP:8080` address printed in the terminal

To stop the server, press `Ctrl+C`.

You can also drop these files on any static host (GitHub Pages, Netlify, a USB web server, etc.). **HTTPS** is required for a full “Install app” prompt on the public internet; `localhost` is enough on this machine.

## What you get

- **Editor** — templates, layout, cover, tables, security
- **Preview** — front and back of each A4 sheet
- **Print / PDF** — from the toolbar, or from the phone’s Print tab
- **Offline** — designs stay in this browser; a service worker keeps the app cached

Your cards are stored on the device (not on a server). Use **Export** / **Import** to move a design between phone and computer.
