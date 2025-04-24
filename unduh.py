import os
import requests
import yt_dlp
import time
from urllib.parse import urlparse
import mimetypes
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.live import Live

console = Console()

def is_youtube(url):
    return any(domain in url for domain in ["youtube.com", "youtu.be"])

def validate_mp3(url):
    if is_youtube(url):
        return True
    try:
        response = requests.head(url, allow_redirects=True, timeout=5)
        content_type = response.headers.get('Content-Type', '')
        return 'audio/mpeg' in content_type or url.lower().endswith('.mp3')
    except:
        return False

def get_safe_filename(filename, download_path):
    base, ext = os.path.splitext(filename)
    counter = 1
    while os.path.exists(os.path.join(download_path, f"{base}({counter}){ext}")):
        counter += 1
    return f"{base}({counter}){ext}" if counter > 1 else filename

def futuristic_animation():
    colors = ["#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4", "#FFEEAD"]
    text = Text("🔥 FUTURISTIC MP3 DOWNLOADER 🔥", style="bold", justify="center")
    
    with Live(console=console, auto_refresh=False) as live:
        for i in range(15):
            text.stylize(colors[i % len(colors)], 0, len(text.plain))
            live.update(Panel(text, width=70, style="on #2C3E50"))
            live.refresh()
            time.sleep(0.08)
    console.clear()

def get_best_audio(url, download_path):
    ffmpeg_path = r'D:\cyber\ffmpeg-2025-04-21-git-9e1162bdf1-full_build\bin'
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(download_path, '%(title)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',
        }],
        'ffmpeg_location': ffmpeg_path,
        'quiet': True,
        'writethumbnail': True,
        'postprocessor_args': ['-metadata', 'title=%(title)s']
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            return f"{info['title']}.mp3"
    except Exception as e:
        console.print(f"[bold red]ERROR:[/bold red] {str(e)}")
        return None

def download_mp3(url, download_path):
    try:
        if is_youtube(url):
            console.print("\n[bold cyan]🔍 Processing YouTube URL...[/bold cyan]")
            return get_best_audio(url, download_path)
        
        else:
            with requests.get(url, stream=True) as r:
                r.raise_for_status()
                filename = os.path.basename(urlparse(url).path)
                filename = filename if filename.endswith('.mp3') else f"{filename}.mp3"
                filename = get_safe_filename(filename, download_path)
                
                total_size = int(r.headers.get('content-length', 0))
                downloaded = 0
                
                with console.status("[bold green]Downloading...[/bold green]") as status:
                    with open(os.path.join(download_path, filename), 'wb') as f:
                        for chunk in r.iter_content(chunk_size=8192):
                            f.write(chunk)
                            downloaded += len(chunk)
                            status.update(
                                f"[cyan]{downloaded/1024:.1f}KB/{total_size/1024:.1f}KB "
                                f"({downloaded/total_size:.2%})[/cyan]"
                            )
                return filename
                
    except Exception as e:
        console.print(f"[bold red]ERROR:[/bold red] {str(e)}")
        return None

def main():
    download_path = "D:\\HQ_MP3_Downloads"
    os.makedirs(download_path, exist_ok=True)
    
    console.clear()
    futuristic_animation()
    
    console.print(Panel.fit(
        "[bold cyan]🎧 MASUKKAN URL YOUTUBE/MP3 🎧[/bold cyan]", 
        width=70, 
        style="cyan"
    ))
    
    url = console.input("\n[bold yellow]>> URL: [/bold yellow]")
    
    if not validate_mp3(url):
        console.print(Panel(
            "[bold red]✖ URL TIDAK VALID![/bold red]",
            style="red",
            width=70
        ))
        return
    
    result = download_mp3(url, download_path)
    
    if result:
        console.print(Panel(
            f"[bold green]✅ BERHASIL![/bold green]\n"
            f"[white]File: {download_path}\\{result}[/white]",
            style="green",
            width=70
        ))
    else:
        console.print(Panel(
            "[bold red]✖ GAGAL![/bold red] Coba cek URL/koneksi",
            style="red",
            width=70
        ))

if __name__ == "__main__":
    main()
