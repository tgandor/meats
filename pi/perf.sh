#!/bin/bash

# vcgencmd commands
# commands="vcos, ap_output_control, ap_output_post_processing, vchi_test_init, vchi_test_exit, pm_set_policy, pm_get_status, pm_show_stats, pm_start_logging, pm_stop_logging, version, commands, set_vll_dir, set_backlight, set_logging, get_lcd_info, arbiter, cache_flush, otp_dump, test_result, codec_enabled, get_camera, get_mem, measure_clock, measure_volts, scaling_kernel, scaling_sharpness, get_hvs_asserts, get_throttled, measure_temp, get_config, hdmi_ntsc_freqs, hdmi_adjust_clock, hdmi_status_show, hvs_update_fields, pwm_speedup, force_audio, hdmi_stream_channels, hdmi_channel_map, display_power, read_ring_osc, memtest, dispmanx_list, get_rsts, schmoo, render_bar, disk_notify, inuse_notify, sus_suspend, sus_status, sus_is_enabled, sus_stop_test_thread, egl_platform_switch, mem_validate, mem_oom, mem_reloc_stats, hdmi_cvt, hdmi_timings, file, vctest_memmap, vctest_start, vctest_stop, vctest_set, vctest_get"

vcgencmd measure_temp
vcgencmd measure_volts
vcgencmd measure_clock arm
vcgencmd get_throttled

