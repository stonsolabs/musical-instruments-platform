# Product Images Guide

Unfortunately, automated downloading from music retailers is challenging due to anti-scraping protections. Here's your best approach to get real product images:

## Manual Download Approach (Recommended)

### For each product, visit these retailer pages and save images:

#### Boss DS-1 Distortion
- **Thomann**: https://www.thomann.de/gb/boss_ds_1_distortion.htm
- **Gear4Music**: https://www.gear4music.com/Guitar-and-Bass/Boss-DS-1-Distortion-Pedal/6QC
- **Andertons**: https://www.andertons.co.uk/boss-ds-1-distortion-pedal

#### Casio PX-560 Digital Piano
- **Thomann**: https://www.thomann.de/gb/casio_px_560_bk.htm
- **Gear4Music**: https://www.gear4music.com/Pianos-and-Keyboards/Casio-PX-560-Digital-Piano-Black/1QYZ

#### Electro-Harmonix Big Muff Pi
- **Thomann**: https://www.thomann.de/gb/electro_harmonix_big_muff_pi.htm
- **Gear4Music**: https://www.gear4music.com/Guitar-and-Bass/Electro-Harmonix-Big-Muff-Pi-Distortion-Sustain-Pedal/5QT

#### Fender Player Jazz Bass
- **Thomann**: https://www.thomann.de/gb/fender_player_jazz_bass_pf_3ts.htm
- **Gear4Music**: https://www.gear4music.com/Guitar-and-Bass/Fender-Player-Jazz-Bass-3-Colour-Sunburst-Pau-Ferro/2ZYX

#### Fender Player Stratocaster
- **Thomann**: https://www.thomann.de/gb/fender_player_strat_pf_pwt.htm
- **Gear4Music**: https://www.gear4music.com/Guitar-and-Bass/Fender-Player-Stratocaster-Polar-White-Pau-Ferro/2ZYW

#### Fender Rumble 40 V3
- **Thomann**: https://www.thomann.de/gb/fender_rumble_40_v3.htm
- **Gear4Music**: https://www.gear4music.com/Guitar-and-Bass/Fender-Rumble-40-V3-Bass-Combo-Amplifier/1VKZ

#### Focusrite Scarlett 2i2 3rd Gen
- **Thomann**: https://www.thomann.de/gb/focusrite_scarlett_2i2_3rd_gen.htm
- **Gear4Music**: https://www.gear4music.com/Recording-and-Computers/Focusrite-Scarlett-2i2-3rd-Gen-USB-Audio-Interface/2YKV

#### Gibson Les Paul Studio
- **Thomann**: https://www.thomann.de/gb/gibson_les_paul_studio_eb_2019.htm
- **Gear4Music**: https://www.gear4music.com/Guitar-and-Bass/Gibson-Les-Paul-Studio-Ebony/3QYX

#### Ibanez SR300E
- **Thomann**: https://www.thomann.de/gb/ibanez_sr300e_pw.htm
- **Gear4Music**: https://www.gear4music.com/Guitar-and-Bass/Ibanez-SR300E-Bass-Guitar-Pearl-White/1ZMX

#### Marshall DSL40CR
- **Thomann**: https://www.thomann.de/gb/marshall_dsl40cr.htm
- **Gear4Music**: https://www.gear4music.com/Guitar-and-Bass/Marshall-DSL40CR-40W-Valve-Guitar-Combo-Amplifier/1XKY

#### Martin D-28 Standard
- **Thomann**: https://www.thomann.de/gb/martin_guitars_d_28_standard.htm
- **Gear4Music**: https://www.gear4music.com/Guitar-and-Bass/Martin-D-28-Standard-Acoustic-Guitar/2VKX

#### Numark Party Mix
- **Thomann**: https://www.thomann.de/gb/numark_party_mix.htm
- **Gear4Music**: https://www.gear4music.com/DJ/Numark-Party-Mix-DJ-Controller/2WKY

#### Pearl Export EXX725SP
- **Thomann**: https://www.thomann.de/gb/pearl_export_standard_725_smokey_chrome.htm
- **Gear4Music**: https://www.gear4music.com/Drums-and-Percussion/Pearl-Export-EXX725SP-C31-5-Piece-Drum-Kit-Smokey-Chrome/3VLZ

#### Pioneer DDJ-SB3
- **Thomann**: https://www.thomann.de/gb/pioneer_dj_ddj_sb3.htm
- **Gear4Music**: https://www.gear4music.com/DJ/Pioneer-DDJ-SB3-DJ-Controller/2XLY

#### Roland TD-17KV
- **Thomann**: https://www.thomann.de/gb/roland_td_17kv_v_drums.htm
- **Gear4Music**: https://www.gear4music.com/Drums-and-Percussion/Roland-TD-17KV-V-Drums-Electronic-Drum-Kit/2YMZ

#### Shure SM57
- **Thomann**: https://www.thomann.de/gb/shure_sm57_lc.htm
- **Gear4Music**: https://www.gear4music.com/Recording-and-Computers/Shure-SM57-LC-Cardioid-Dynamic-Microphone/VKX

#### Yamaha FG830
- **Thomann**: https://www.thomann.de/gb/yamaha_fg830_nt.htm
- **Gear4Music**: https://www.gear4music.com/Guitar-and-Bass/Yamaha-FG830-Acoustic-Guitar-Natural/1WLX

#### Yamaha P-125
- **Thomann**: https://www.thomann.de/gb/yamaha_p_125_bk.htm
- **Gear4Music**: https://www.gear4music.com/Pianos-and-Keyboards/Yamaha-P-125-Digital-Piano-Black/2XMY

## How to Save Images:

1. **Visit the retailer page**
2. **Right-click on product images**
3. **Save as** with these exact filenames:
   - `{product_name}_1.jpg` (main product image)
   - `{product_name}_2.jpg` (side/angle view)
   - `{product_name}_3.jpg` (close-up/details)
   - `{product_name}_4.jpg` (back/additional view)

4. **Save to**: `./frontend/public/product-images/`

## Alternative: API-Based Solutions

If you want to try automated downloading, you can:

1. **Get a free Pixabay API key**: https://pixabay.com/api/docs/
2. **Edit `download_product_images_final.py`** and add your API key
3. **Run**: `python3 download_product_images_final.py`

Or:

1. **Get a free Pexels API key**: https://www.pexels.com/api/
2. **Edit `download_product_images_pexels.py`** and add your API key  
3. **Run**: `python3 download_product_images_pexels.py`

## Why Automated Scraping Failed:

- Modern e-commerce sites have strong anti-scraping protections
- Dynamic loading and JavaScript-heavy interfaces
- Rate limiting and IP blocking
- CAPTCHA and bot detection systems

## Best Practice:

For a commercial project, the most reliable approach is:
1. **Manual download** from retailer websites (as shown above)
2. **Contact manufacturers** for press kit images
3. **Purchase stock photos** from professional services
4. **Use manufacturer official images** with proper attribution