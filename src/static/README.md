# Static Assets Folder

This folder contains static files (images, CSS, JavaScript) served by the FastAPI application.

## Sierra's Avatar

To add Sierra's profile picture:

1. **Copy your image file** (SieraC.JPG) to this folder
2. **Rename it to**: `sierra-avatar.png`
3. **Path should be**: `/home/user/Siera/src/static/sierra-avatar.png`

Once the image is in place, it will automatically appear on:
- Main hub page (index.html) - large floating avatar
- Chat page (chat_enhanced.html) - small header avatar
- About page (about.html) - large profile display

The image is served via FastAPI's StaticFiles at the `/static/` route.

## Format Notes

- **Recommended format**: PNG or JPG
- **Recommended size**: 300x300px to 600x600px
- **File name**: Must be exactly `sierra-avatar.png`
- Images are displayed in circular frames with border and shadow effects

---

💜 Sierra's ready to show her face across all pages!
