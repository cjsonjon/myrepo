import os
import subprocess
import hashlib
import json
import shlex
from flask import Flask, request, render_template, send_file, redirect, url_for,  jsonify, send_from_directory
from gtts import gTTS

from flask_lt import run_with_lt
from flask_cors import CORS



app = Flask(__name__)



# --------------------------
# Your phrase -> video map
# --------------------------
WORD_TO_VIDEO = {
    "chung toi": "videos/1_chung_toi.mp4",
    "dia chi": "videos/2_dia_chi.mp4",
    "khong can": "videos/3_khong_can.mp4",
    "nhan vien": "videos/4_sl_nhan_vien.mp4",
    "nhap khau": "videos/5_sl_nhap_khau.mp4",
    "lung tung": "videos/6_sl_lung_tung.mp4",
    "khuyen khich": "videos/7_sl_khuyen_khich.mp4",
    "hap dan": "videos/8_sl_hap_dan.mp4",
    "my tom": "videos/9_my_tom.mp4",
    "nau nuong": "videos/10_nau_nuong.mp4",
    "com rang": "videos/11_com_rang.mp4",
    "ong ba": "videos/12_ong_ba.mp4",
    "ho": "videos/13_ho.mp4",
    "di dao": "videos/15_di_dao.mp4",
    "em ho": "videos/16_em_ho.mp4",
    "hen": "videos/17_hen.mp4",
    "moi ngay": "videos/18_moi_ngay.mp4",
    "danh rang": "videos/19_danh_rang_problem.mp4",
    "cuoi tuan": "videos/20_cuoi_tuan.mp4",
    "cuoi thang": "videos/21_cuoi_thang.mp4",
    "cuoi nam": "videos/22_cuoi_nam.mp4",
    "muc tieu": "videos/23_muc_tieu.mp4",
    "mo ta": "videos/24_mo_ta.mp4",
    "do an": "videos/25_do_an.mp4",
    "do uong": "videos/26_do_uong.mp4",
    "ban bac": "videos/28_ban_bac.mp4",
    "bao tang": "videos/29_bao_tang.mp4",
    "bao cao": "videos/30_bao_cao_problem.mp4",
    "bao dong": "videos/31_bao_dong.mp4",
    "di ve": "videos/32_di_ve.mp4",
    "bac bo": "videos/33_bac_bo.mp4",
    "bat tay": "videos/35_bat_tay.mp4",
    "be hon": "videos/36_be_hon.mp4",
    "be boi": "videos/37_be_boi.mp4",
    "bia dat": "videos/38_bia_dat.mp4",
    "binh thuong": "videos/41_binh_thuong_problem.mp4",
    "nghi he": "videos/45_nghi_he.mp4",
    "truoc": "videos/46_truoc.mp4",
    "ca kho": "videos/50_ca_kho.mp4",
    "cao tang": "videos/54_cao_tang.mp4",
    "o ngoai": "videos/55_o_ngoai.mp4",
    "cau thu": "videos/56_cau_thu - Trim.mp4",
    "cheo thuyen": "videos/58_cheo_thuyen.mp4",
    "chep bai": "videos/59_chep_bai.mp4",
    "chi tiet": "videos/60_chi_tiet.mp4",
    "chi huy": "videos/62_chi_huy.mp4",
    "chi dau": "videos/63_chi_dau.mp4",
    "chia se": "videos/64_chia_se.mp4",
    "chia tay": "videos/65_chia_tay.mp4",
    "chia khoa": "videos/66_chia_khoa.mp4",
    "chien thang": "videos/67_chien_thang.mp4",
    "luc nao": "videos/69_luc_nao.mp4",
    "muon": "videos/70_muon.mp4",
    "chon loc": "videos/73_chon_loc.mp4",
    "co quan": "videos/74_co_quan.mp4",
    "coi mo": "videos/75_coi_mo.mp4",
    "dan nhac": "videos/78_dan_nhac.mp4",
    "day nha": "videos/80_day_nha.mp4",
    "em re": "videos/82_em_re.mp4",
    "ghe tham": "videos/83_ghe_tham.mp4",
    "giao hang": "videos/85_giao_hang.mp4",
    "giao luu": "videos/86_giao_luu.mp4",
    "gioi": "videos/87_gioi.mp4",
    "gioi thieu": "videos/88_gioi_thieu.mp4",
    "gon gang": "videos/89_gon_gang.mp4",
    "hop dong": "videos/93_hop_dong.mp4",
    "kho khan": "videos/94_kho_khan.mp4",
    "kiem tra": "videos/97_kiem_tra.mp4",
    "lam quen": "videos/99_lam_quen.mp4",
    "bit tet": "videos/101_bit_tet.mp4",
    "boi roi": "videos/102_boi_roi.mp4",
    "bo tro": "videos/103_bo_tro.mp4",
    "buc minh": "videos/105_buc_minh.mp4",
    "bun cha": "videos/106_bun_cha.mp4",
    "bun dau": "videos/107_bun_dau.mp4",
    "bun oc": "videos/109_bun_oc.mp4",
    "but bi": "videos/110_but_bi.mp4",
    "chao suon": "videos/114_chao_suon.mp4",
    "chien khu": "videos/115_chien_khu.mp4",
    "chieu cao": "videos/116_chieu_cao.mp4",
    "chieu dai": "videos/117_chieu_dai.mp4",
    "chi ho": "videos/119_chi_ho.mp4",
    "cua khau": "videos/120_cua_khau.mp4",
    "ghen ti": "videos/122_ghen_ti.mp4",
    "kip thoi": "videos/126_kip_thoi.mp4",
    "ky nang": "videos/128_ky_nang.mp4",
    "macau": "videos/129_Macau.mp4",
    "may man": "videos/130_may_man.mp4",
    "my y": "videos/132_my_y.mp4",
    "nhan manh": "videos/134_nhan_manh.mp4",
    "song sot": "videos/136_song_sot.mp4",
    "them": "videos/137_them.mp4",
    "thoi quen": "videos/139_thoi_quen.mp4",
    "tu choi": "videos/140_tu_choi.mp4",
    "xoi ga": "videos/143_xoi_ga.mp4",
    "an du": "videos/145_an_du.mp4",
    "gap ba": "videos/146_gap_ba.mp4",
    "gap doi": "videos/147_gap_doi.mp4",
    "an giang": "videos/149_An_giang.mp4",
    "ao phong": "videos/151_ao_phong.mp4",
    "ao phao": "videos/152_ao_phao.mp4"
}
# keep sorted for display
WORD_TO_VIDEO = dict(sorted(WORD_TO_VIDEO.items()))

COMBINED_DIR = "combined_videos"
PROCESSED_DIR = "processed_videos"
os.makedirs(COMBINED_DIR, exist_ok=True)
os.makedirs(PROCESSED_DIR, exist_ok=True)

# --------------------------
# Helpers: tokenization / segmentation (unchanged)
# --------------------------
MAX_PHRASE_LEN = max(len(k.split()) for k in WORD_TO_VIDEO)


@app.route('/frames/<pose_name>')
def list_frames(pose_name):
    """
    Returns JSON: { "frames": [url1, url2, ...] }
    Works for:
      - static/poses/<pose_name>/000001.obj  (flat)
      - static/poses/<pose_name>/000001/000.obj (per-frame folders)
    Sorts frames by name (lexicographically) which works with zero-padded names.
    """
    base = os.path.join('static', 'poses', pose_name)
    if not os.path.isdir(base):
        return jsonify({"error": "pose not found"}), 404

    # 1) try flat .obj files directly inside base
    flat_objs = sorted([f for f in os.listdir(base) if f.lower().endswith('.obj')])
    urls = []
    if flat_objs:
        for f in flat_objs:
            urls.append(url_for('static', filename=f'poses/{pose_name}/{f}'))
        return jsonify({"frames": urls})

    # 2) fallback: treat every immediate child dir as a frame and find first .obj inside it
    entries = sorted([d for d in os.listdir(base) if os.path.isdir(os.path.join(base, d))])
    for d in entries:
        dpath = os.path.join(base, d)
        # find first .obj in that folder (sorted)
        objs = sorted([f for f in os.listdir(dpath) if f.lower().endswith('.obj')])
        if objs:
            rel = f'poses/{pose_name}/{d}/{objs[0]}'
            urls.append(url_for('static', filename=rel))
    if not urls:
        return jsonify({"frames": [], "warning": "no .obj files found"}), 200
    return jsonify({"frames": urls})

def tokenize(s):
    return s.strip().lower().split()

def segment_phrase(tokens):
    i, N = 0, len(tokens)
    segments = []
    while i < N:
        matched = False
        for L in range(MAX_PHRASE_LEN, 0, -1):
            if i+L > N: continue
            cand = " ".join(tokens[i:i+L])
            if cand in WORD_TO_VIDEO:
                segments.append(cand)
                i += L
                matched = True
                break
        if not matched:
            return None
    return segments

# --------------------------
# ffmpeg concat (robust)
# --------------------------
def ffmpeg_concat(video_paths, out_dir=COMBINED_DIR):
    os.makedirs(out_dir, exist_ok=True)
    name = "_".join(os.path.splitext(os.path.basename(p))[0] for p in video_paths)
    h = hashlib.sha1(name.encode()).hexdigest()[:8]
    outp = os.path.join(out_dir, f"{name}_{h}.mp4")
    if os.path.isfile(outp):
        return outp

    list_file = os.path.join(out_dir, f"list_{h}.txt")
    with open(list_file, "w") as f:
        for p in video_paths:
            f.write(f"file '{os.path.abspath(p)}'\n")

    # try fast copy concat first
    cmd = ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", list_file, "-c", "copy", outp]
    p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if p.returncode != 0:
        # fallback: re-encode while concatenating
        cmd_re = ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", list_file,
                  "-c:v", "libx264", "-pix_fmt", "yuv420p",
                  "-c:a", "aac", "-b:a", "64k", outp]
        p2 = subprocess.run(cmd_re, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if p2.returncode != 0:
            raise RuntimeError("ffmpeg concat failed:\n" + p2.stderr.decode())
    return outp

# --------------------------
# Process video: filters, subtitles, TTS
# --------------------------
def process_video(input_video, brightness=0.0, contrast=1.0, saturation=1.0,
                  subtitle_text=None, tts_text=None, tint_color=None, tint_strength=0.0):
    """
    Simplified video processing using a single -vf chain (no slow filter_complex).
    Adds:
      - eq (brightness/contrast)
      - hue (saturation)
      - optional simple tint implemented with lutrgb blending (fast)
      - optional drawtext subtitles
      - optional TTS muxing (unchanged)
    tint_color: hex like '#ff3366' or 'ff3366'
    tint_strength: 0.0..1.0 (0 = no tint, 1 = full replace with tint color)
    """
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    base = os.path.splitext(os.path.basename(input_video))[0]
    args_hash = hashlib.sha1(f"{base}_{brightness}_{contrast}_{saturation}_{subtitle_text}_{tts_text}_{tint_color}_{tint_strength}".encode()).hexdigest()[:8]
    outp = os.path.join(PROCESSED_DIR, f"{base}_proc_{args_hash}.mp4")
    if os.path.isfile(outp):
        return outp

    # Build a simple -vf chain (eq -> hue -> optional lutrgb tint -> optional drawtext)
    vf_parts = []
    vf_parts.append(f"eq=brightness={brightness}:contrast={contrast}")
    vf_parts.append(f"hue=s={saturation}")

    # Simple tint using lutrgb (fast). This blends each channel towards the tint color:
    # new = src*(1-t) + (tint*255)*t
    try:
        ts = float(tint_strength)
    except:
        ts = 0.0

    if tint_color and ts > 0.0001:
        hexcol = tint_color.strip()
        if hexcol.startswith("#"):
            hexcol = hexcol[1:]
        if len(hexcol) == 6:
            tr = int(hexcol[0:2], 16) / 255.0
            tg = int(hexcol[2:4], 16) / 255.0
            tb = int(hexcol[4:6], 16) / 255.0
        else:
            # fallback to red
            tr, tg, tb = 1.0, 0.0, 0.0

        # clamp tint_strength to [0,1]
        if ts < 0.0: ts = 0.0
        if ts > 1.0: ts = 1.0

        # Precompute 0-255 tint components
        tr255 = round(tr * 255, 6)
        tg255 = round(tg * 255, 6)
        tb255 = round(tb * 255, 6)

        # If your ffmpeg applies channels as BGR in this filter, set swap_rb=True to fix red/blue swap.
        swap_rb = True

        if swap_rb:
            # map the parsed R->B and B->R to correct the swap
            r_target = tb255
            g_target = tg255
            b_target = tr255
        else:
            r_target = tr255
            g_target = tg255
            b_target = tb255

        # Use 'val' (current channel value) in lut expressions
        r_expr = f"val*(1-{ts})+{r_target}*{ts}"
        g_expr = f"val*(1-{ts})+{g_target}*{ts}"
        b_expr = f"val*(1-{ts})+{b_target}*{ts}"

        # Add lut filter (use quotes around expressions)
        vf_parts.append(f"lut=r='{r_expr}':g='{g_expr}':b='{b_expr}'")

    # drawtext (if provided) - keep it simple & robust
    if subtitle_text:
        fontfile = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
        txt = subtitle_text.replace(":", "\\:").replace("'", "\\'")
        #draw = (f"drawtext=fontfile={fontfile}:text='{txt}':"
        #        "fontcolor=white:fontsize=36:box=1:boxcolor=black@0.5:"
        #        "x=(w-text_w)/2:y=h-(text_h*2)-30")
        draw = (f"drawtext=fontfile={fontfile}:text='{txt}':"
        "fontcolor=white:fontsize=36:box=1:boxcolor=black@0.5:"
        "x=(w-text_w)/2:y=text_h+20")
        vf_parts.append(draw)

    vf = ",".join(vf_parts)

    # If TTS requested, synthesize mp3 and then map it as audio
    tts_file = None
    if tts_text:
        tts_hash = hashlib.sha1(tts_text.encode()).hexdigest()[:8]
        tts_file = os.path.join(PROCESSED_DIR, f"tts_{tts_hash}.mp3")
        if not os.path.isfile(tts_file):
            tts = gTTS(tts_text, lang='vi')
            tts.save(tts_file)

    # Encode with the simple -vf chain (single filter string — faster than complex graphs)
    tmp_out = os.path.join(PROCESSED_DIR, f"{base}_tmp_{args_hash}.mp4")
    cmd = [
        "ffmpeg", "-y", "-i", input_video,
        "-vf", vf,
        "-c:v", "libx264", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "64k", tmp_out
    ]
    run = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if run.returncode != 0:
        raise RuntimeError("ffmpeg filter failed:\n" + run.stderr.decode())

    # If there is tts audio, mux it (replace audio)
    if tts_file:
        cmd2 = [
            "ffmpeg", "-y", "-i", tmp_out, "-i", tts_file,
            "-map", "0:v", "-map", "1:a",
            "-c:v", "copy", "-c:a", "aac",  outp
        ]
        p2 = subprocess.run(cmd2, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if p2.returncode != 0:
            raise RuntimeError("ffmpeg mux tts failed:\n" + p2.stderr.decode())
        try:
            os.remove(tmp_out)
        except: pass
    else:
        os.rename(tmp_out, outp)

    return outp


# --------------------------
# Routes
# --------------------------
@app.route('/', methods=['GET','POST'])
def index():
    video_url, human_input = None, None
    error = None

    if request.method == 'POST':
        human_input = request.form.get('word', '').strip()
        tokens = tokenize(human_input)
        segments = segment_phrase(tokens)
        if segments is None:
            error = "Could not parse input into known words/phrases."
        else:
            if len(segments) == 1:
                video_url = WORD_TO_VIDEO.get(segments[0])
            else:
                vids = [WORD_TO_VIDEO[s] for s in segments]
                try:
                    video_url = ffmpeg_concat(vids)
                except Exception as e:
                    error = f"Concatenation error: {e}"

    return render_template('index.html', video=video_url, text=human_input, error=error, WORD_TO_VIDEO=WORD_TO_VIDEO)

@app.route('/process', methods=['POST'])
def process():
    """
    Takes form fields:
    - video (path returned by concat or direct)
    - brightness (-1..1)
    - contrast (0..2)
    - saturation (0..3)
    - tint_color (e.g. #ff0000)
    - tint_strength (0..1)
    - subtitle (text)
    - tts (on/off)
    Returns processed video path and plays it.
    """
    video = request.form.get('video_path')
    if not video or not os.path.isfile(video):
        return "Invalid video path", 400

    # parse filters
    def safe_float(name, default):
        try:
            return float(request.form.get(name, default))
        except:
            return default

    brightness = safe_float('brightness', 0.0)
    contrast   = safe_float('contrast', 1.0)
    saturation = safe_float('saturation', 1.0)

    # NEW: tint fields
    tint_color = request.form.get('tint_color', '').strip() or None
    tint_strength = safe_float('tint_strength', 0.0)

    subtitle   = request.form.get('subtitle', '').strip() or None
    tts_on     = request.form.get('tts', 'off') == 'on'
    tts_text   = request.form.get('tts_text', subtitle if subtitle else None) if tts_on else None

    try:
        proc = process_video(
            video,
            brightness=brightness,
            contrast=contrast,
            saturation=saturation,
            subtitle_text=subtitle,
            tts_text=tts_text,
            tint_color=tint_color,           # pass tint color
            tint_strength=tint_strength      # pass tint strength
        )
    except Exception as e:
        return f"Processing failed: {e}", 500

    # return processed page so user can play/download
    return render_template('index.html', video=proc, text=request.form.get('original_input',''), WORD_TO_VIDEO=WORD_TO_VIDEO)


@app.route('/video/<path:fn>')
def video(fn):
    # allow absolute path serving (ensure safety in production)
    if os.path.isabs(fn) and os.path.isfile(fn):
        return send_file(fn, mimetype='video/mp4')
    # else treat as relative path
    safe_path = os.path.join('.', fn)
    if os.path.isfile(safe_path):
        return send_file(safe_path, mimetype='video/mp4')
    return "Not found", 404

if __name__ == '__main__':
    #app.run(debug=True)
    app.run(host='0.0.0.0', port=5000, debug=True)
