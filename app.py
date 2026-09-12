from flask import Flask, request, jsonify, send_file
import yt_dlp
import os

app = Flask(__name__)

@app.route('/download', methods=['GET'])
def download_video():
    url = request.args.get('url')
    file_format = request.args.get('format', 'mp3')
    
    if not url:
        return jsonify({"error": "No URL provided"}), 400

    # กำหนดค่าคอนฟิกของ yt-dlp พร้อมใส่คุกกี้เพื่อป้องกันการบล็อก
    ydl_opts = {
        'format': 'bestaudio/best' if file_format == 'mp3' else 'best',
        'cookiefile': 'cookies.txt',  # <--- จุดสำคัญที่เพิ่มเข้ามาเพื่อแก้ปัญหา Bot Block
        'outtmpl': '%(id)s.%(ext)s',
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            
            # ถ้าต้องการแปลงเป็น mp3 สามารถใส่โค้ดจัดการไฟล์เพิ่มเติมตรงนี้ได้ตามระบบเดิมของคุณ
            return send_file(filename, as_attachment=True)
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
