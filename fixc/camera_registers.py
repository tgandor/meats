import re
from itertools import groupby

register_defs = """
#define mcu_variable_address 0x098E
#define mcu_variable_data 0x0990

#define pll_dividers_reg 0x0010
#define pll_p_dividers_reg 0x0012
#define pll_control_reg 0x0014
#define standby_control_and_status_reg 0x0018
#define reset_and_misc_control_reg 0x001a
#define pad_slew_pad_config_reg 0x001e
#define vdd_dis_counter_reg 0x0022
#define pll_p4_p5_p6_dividers_reg 0x002a
#define sensor_clock_divider_reg 0x002e
#define i2c_master_control 0x3b82
#define i2c_master_frequency_divider 0x3b84
#define second_scl_sda_pd 0x0614
"""

to_translate = """
            {0x001a , 0x0219},
            {0x001a , 0x0018},
            //reset camera
            {BEEF_REG , 100 },
            {pll_control_reg , 0x2425},
            {pll_control_reg , 0x2145},
            {0x0010 , 0x0110},
            {0x0012 , 0x00f0},
            {0x002a , 0x7f77},
            {pll_control_reg , 0x2545},
            {pll_control_reg , 0x2547},
            {pll_control_reg , 0x3447},
            {pll_control_reg , 0x3047},
            {BEEF_REG , 10 },       // delay(10);
            {pll_control_reg , 0x3046},
            {0x0022 , 0x01f4},
            {0x001e , 0x0707},
            {0x3b84 , 0x01f4},
            {0x002e , 0x0500},
            {0x0018 , 0x402b},
            {0x3b82 , 0x0004},
            {0x0018 , 0x402f},
            {0x0018 , 0x402e},
"""

to_translate = """
            {BEEF_REG , 50 },       // delay(50);
            {0x0614 , 0x0001},
            {BEEF_REG , 1 },        // delay(1);
            {0x0614 , 0x0001},
            {BEEF_REG , 1 },        // delay(1);
            {0x0614 , 0x0001},
            {BEEF_REG , 1 },        // delay(1);
            {0x0614 , 0x0001},
            {BEEF_REG , 1 },        // delay(1);
            {0x0614 , 0x0001},
            {BEEF_REG , 1 },        // delay(1);
            {0x0614 , 0x0001},
            {BEEF_REG , 1 },        // delay(1);
            {BEEF_REG , 10 },       // delay(10);
"""

to_translate = """
            {0x0018 , 0x002a},
            {0x3084 , 0x2409},
            {0x3092 , 0x0a49},
            {0x3094 , 0x4949},
            {0x3096 , 0x4950},
            
            {0x316c , 0x350f},
            {0x001e , 0x0777},
"""

EXTCLK = 12.

regHex = '0x[0-9A-Fa-f]'
fourHex = regHex + '{4}'


def translate(to_translate):
    registers = []
    register_names = {}
    register_names_set = set()
    unknown = set()
    for defn in register_defs.split('\n'):
        if not defn.strip():
            continue
        _, name, value = defn.split()
        registers.append(value)
        register_names[value] = name
        register_names_set.add(name)
    result = []
    for line in to_translate.split('\n'):
        found = False
        for register in registers:
            if '{' + register in line:
                result.append(line.replace('{' + register, '{' + register_names[register]))
                found = True
                break
        if not found:
            result.append(line)
            match = re.search('\{(\w+)', line)
            if match:
                unknown.add(match.group(1))
    print('Unknown registers: {}'.format(' '.join(sorted(unknown - register_names_set))))
    return '\n'.join(result)


# print translate(to_translate)


def _get_bits(val, start, end=None):
    if end is None:
        return (val & (1 << start)) >> start
    mask = (1 << (start - end + 1)) - 1
    return (val >> end) & mask


def pll_control_reg(val):
    if type(val) != int:
        val = int(val, 16)
    # print(val)
    # print('clockin_hyst_enable={}'.format(_get_bits(val, 13)))
    # print('test_bypass={}'.format(_get_bits(val, 10)))
    # print('reset_cntr={}'.format(_get_bits(val, 8)))
    # print('pll_enable={}'.format(_get_bits(val, 1)))
    # print('pll_bypass={}'.format(_get_bits(val, 0)))
    return [
    'clockin_hyst_enable={}'.format(_get_bits(val, 13)),
    'test_bypass={}'.format(_get_bits(val, 10)),
    'reset_cntr={}'.format(_get_bits(val, 8)),
    'pll_enable={}'.format(_get_bits(val, 1)),
    'pll_bypass={}'.format(_get_bits(val, 0)),
    ]

def pll_dividers_reg(val):
    if type(val) != int:
        val = int(val, 16)
    return [
    'n={}'.format(_get_bits(val, 13, 8)),
    'm={}'.format(_get_bits(val, 7, 0))
    ]

def BEEF_REG(val):
    return ['delay({})'.format(val)]

#
# VARs
#

def var_id_offset(n):
    if n & 0x8000:
        n ^= 0x8000
    return n >> 10, n & ((1 << 10) - 1)

def var(n):
    vartype = "VAR"
    if n & 0x8000:
        vartype = "VAR8"
    id_, offset = var_id_offset(n)
    return ("{}({},{})".format(vartype, id_, offset))

def VAR(id_, offset):
    return (id_ << 10) + offset
def VAR8(id_, offset):
    return (id_ << 10) + offset + 0x8000

to_set_var = """
            {0x098e , 0x68a0},
            {0x0990 , 0x0a2e},
            {0x098e , 0x6ca0},
            {0x0990 , 0x0a2e},
            {0x098e , 0x6c90},
            {0x0990 , 0x0cb4},
            {0x098e , 0x6807},
            {0x0990 , 0x0004},
            {0x098e , 0xe88e},
            {0x0990 , 0x0000},
            {0x316c , 0x350f},
            {0x001e , 0x0777},
            {0x098e , 0x8400},
            {0x0990 , 0x0001},
            {BEEF_REG , 100 },      // delay(100);
            {0x098e , 0x8400},
            {0x0990 , 0x0006},
"""

def convert_to_set_var(data):
    lines = data.split('\n')
    last_var = 0
    for line in lines:
        if not line.strip():
            print('')
            continue
        values = re.findall(fourHex, line)
        if len(values) != 2:
            print(line)
            continue
        reg, val = [int(x, 16) for x in values]
        if reg == 0x098e:
            last_var = val
        elif reg == 0x0990:
            print('            SET_VAR({:13s}, 0x{:04x}),'.format(
                    var(last_var), val
                ))
        else:
            print(line)
# convert_to_set_var(to_set_var)

def var_desc(id_, offset, val, val_vars={}):
    if len(val_vars) == 0: # init
        class VAR:
            def __init__(self, id_, offset):
                self.id_ = id_
                self.offset = offset
            def __le__(self, val):
                val_vars[(self.id_, self.offset)] = val
                return False
        VAR(18, 68) <= 'cam1_ctx_a_fdperiod_50hz'
        VAR(18, 69) <= 'cam1_ctx_a_fdperiod_60hz'
        VAR(18, 68+72) <= 'cam1_ctx_b_fdperiod_50hz'
        VAR(18, 69+72) <= 'cam1_ctx_b_fdperiod_60hz'
        VAR(18,301) <= 'cam1_flash_fd_60hz_prd_msb_cntxt_a'
        VAR(18,302) <= 'cam1_flash_fd_60hz_prd_msb_cntxt_b'
        VAR(18,303) <= 'cam1_flash_fd_50hz_prd_msb_cntxt_a'
        VAR(18,304) <= 'cam1_flash_fd_50hz_prd_msb_cntxt_b'
        VAR(18,142) <= 'cam1_ctx_b_rx_fifo_trigger_mark'

    if id_==18 and offset==12:
        return [
        'cam1_ctx_a:',
        '_x_bin_en={}'.format(_get_bits(val, 11)),
        '_xy_bin_en={}'.format(_get_bits(val, 10)),
        '_low_power={}'.format(_get_bits(val, 9)),
        '_x_oddaddr_inc={}'.format(_get_bits(val, 7, 5)),
        '_y_oddaddr_inc={}'.format(_get_bits(val, 4, 2)),
        '_vert_flip={}'.format(_get_bits(val, 1)),
        '_horiz_mirror={}'.format(_get_bits(val, 0)),
        ]
    
    if id_==18 and offset==12+72:
        return [
        'cam1_ctx_a:',
        '_x_bin_en={}'.format(_get_bits(val, 11)),
        '_xy_bin_en={}'.format(_get_bits(val, 10)),
        '_low_power={}'.format(_get_bits(val, 9)),
        '_x_oddaddr_inc={}'.format(_get_bits(val, 7, 5)),
        '_y_oddaddr_inc={}'.format(_get_bits(val, 4, 2)),
        '_vert_flip={}'.format(_get_bits(val, 1)),
        '_horiz_mirror={}'.format(_get_bits(val, 0)),
        ]
    
    if id_ in (26, 27) and offset==160:
        return [
        'pri_a_config_jpeg_ob_:' if id_ == 26 else 'pri_b_config_jpeg_ob_:',
        'enable_resolution={}'.format(_get_bits(val, 15)),
        'enable_mipi_line_byte_cnt={}'.format(_get_bits(val, 14)),
        'enable_index_table={}'.format(_get_bits(val, 13)),
        'en_legalize_status={}'.format(_get_bits(val, 12)),
        'en_clk_b2_lines={}'.format(_get_bits(val, 11)),
        'insert_ccir_codes={}'.format(_get_bits(val, 10)),
        'insert_jp_status={}'.format(_get_bits(val, 9)),
        'dup_fv_on_lv={}'.format(_get_bits(val, 8)),
        'en_byte_swap={}'.format(_get_bits(val, 7)),
        'en_adaptive_clk={}'.format(_get_bits(val, 6)),
        'soi_eoi_in_fv={}'.format(_get_bits(val, 5)),
        'en_soi_eoi={}'.format(_get_bits(val, 4)),
        'en_clk_invalid_data={}'.format(_get_bits(val, 3)),
        'en_clk_b2_frames={}'.format(_get_bits(val, 2)),
        'tx_mode={}'.format(_get_bits(val, 1, 0)),
        ]

    if id_ in (26, 27) and offset==17:
        return [
        'pri_a_config_fd_algo_run_:' if id_ == 26 else 'pri_b_config_fd_algo_run_:',
        'setperiod={}'.format(_get_bits(val, 1)),
        'detectperiod={}'.format(_get_bits(val, 0)),
        ]
    
    if id_ in (26, 27) and offset==142:
        return [
        'pri_a_config_jpeg_:' if id_ == 26 else 'pri_b_config_jpeg_:',
        'tn_enable={}'.format(_get_bits(val, 1)),
        'jp_enable={}'.format(_get_bits(val, 0)),
        ]
    
    if id_ in (26, 27) and offset==7:
        return [
        'pri_a_of_ (o/format):' if id_ == 26 else 'pri_a_of_ (o/format):',
        'mono={}'.format(_get_bits(val, 9)),
        'processed_bayer={}'.format(_get_bits(val, 8)),
        'raw10={}'.format(_get_bits(val, 6)),
        'raw8={}'.format(_get_bits(val, 5)),
        'rgb444x={}'.format(_get_bits(val, 4)),
        'rgb555x={}'.format(_get_bits(val, 3)),
        'rgb565={}'.format(_get_bits(val, 2)),
        'yuv422={}'.format(_get_bits(val, 0)),
        ]
    
    if id_ in (26, 27) and offset==144:
        return [
        'pri_a_config_jpeg_jp_cfg_' if id_ == 26 else 'pri_b_config_jpeg_jp_cfg_:',
        'frm_ovflw_protect={}'.format(_get_bits(val, 15)),
        'tn_insert_hdr={}'.format(_get_bits(val, 14)),
        'tn_output_ycbcr={}'.format(_get_bits(val, 13)),
        'aqle={}'.format(_get_bits(val, 12)),
        'hdr={}'.format(_get_bits(val, 11, 10)),
        'speedtags_en={}'.format(_get_bits(val, 9)),
        'tn_output_format={}'.format(_get_bits(val, 8)),
        'stat_before_len={}'.format(_get_bits(val, 7)),
        'qtbl_ptr={}'.format(_get_bits(val, 6)),
        'qtbl_autosel={}'.format(_get_bits(val, 5)),
        'qscale_enable={}'.format(_get_bits(val, 4)),
        'tn_swap_chroma={}'.format(_get_bits(val, 3)),
        'retry_enable={}'.format(_get_bits(val, 2)),
        'tn_swap_luma_chroma={}'.format(_get_bits(val, 1)),
        'tn_disable_marker={}'.format(_get_bits(val, 0)),
        ]

    # TODO: val_vars
    if id_==18 and offset==15: return ['cam1_ctx_a_fine_correction = {}'.format(val)]
    if id_==18 and offset==17: return ['cam1_ctx_a_fine_itmin = {}'.format(val)]
    if id_==18 and offset==19: return ['cam1_ctx_a_fine_itmax_margin = {}'.format(val)]
    if id_==18 and offset==29: return ['cam1_ctx_a_base_frame_length_lines = {}'.format(val)]
    if id_==18 and offset==31: return ['cam1_ctx_a_min_line_length_pclk = {}'.format(val)]
    if id_==18 and offset==37: return ['cam1_ctx_a_line_length_pck = {}'.format(val)]

    if id_==18 and offset==15+72: return ['cam1_ctx_b_fine_correction = {}'.format(val)]
    if id_==18 and offset==17+72: return ['cam1_ctx_b_fine_itmin = {}'.format(val)]
    if id_==18 and offset==19+72: return ['cam1_ctx_b_fine_itmax_margin = {}'.format(val)]
    if id_==18 and offset==29+72: return ['cam1_ctx_b_base_frame_length_lines = {}'.format(val)]
    if id_==18 and offset==31+72: return ['cam1_ctx_b_min_line_length_pclk = {}'.format(val)]
    if id_==18 and offset==37+72: return ['cam1_ctx_b_line_length_pck = {}'.format(val)]

    if id_==18 and offset==70: return ['cam1_ctx_a_fifo_trigger_mark = {}'.format(val)]
    if id_==18 and offset==17: return ['cam1_ctx_a_fine_itmin = {}'.format(val)]

    if id_==18 and offset==165: return ['cam1_fd_search_f1_50 = {} (Hz?)'.format(val)]
    if id_==18 and offset==166: return ['cam1_fd_search_f2_50 = {} (Hz?)'.format(val)]
    if id_==18 and offset==167: return ['cam1_fd_search_f1_60 = {} (Hz?)'.format(val)]
    if id_==18 and offset==168: return ['cam1_fd_search_f2_60 = {} (Hz?)'.format(val)]

    if (id_, offset) in val_vars:
        return ['{} = {}'.format(val_vars[(id_, offset)], val)]

    return ["I don't know this variable yet..."]

def var_desc_addr(address, val):
    id_, offset = var_id_offset(address)
    return var_desc(id_, offset, val)

def SET_VAR(address, val):
    print('            SET_VAR({:13s}, 0x{:04x}), // {}'.format(
        var(address), val, ' '.join(var_desc_addr(address, val))
    ))


SET_VAR(VAR(27,144)  , 0x0cb4),
SET_VAR(VAR(26,7)    , 0x0004),
SET_VAR(VAR8(26,142) , 0x0000),

def _pll_init():
    print('**** Default')
    pll_control_reg(0x2425) # default
    print('**** We')
    pll_control_reg(0x2145)
    print('**** Linux')
    pll_control_reg(0x2525)
    pll_control_reg(0x2527)
    pll_control_reg(0x3427)
    pll_control_reg(0x3027)

#
# REG Description functions
#

def pll_p4_p5_p6_dividers_reg(val):
    return [
    '[p6_en={}]'.format(_get_bits(val, 14)),
    'p5_en={}'.format(_get_bits(val, 13)),
    'p4_en={}'.format(_get_bits(val, 12)),
    '[p6={}]'.format(_get_bits(val, 11, 8)),
    'p5={}'.format(_get_bits(val, 7, 4)),
    'p4={}'.format(_get_bits(val, 3, 0)),
    ]

def pll_p_dividers_reg(val):
    return [
    'p3={}'.format(_get_bits(val, 11, 8)),
    'p2={}'.format(_get_bits(val, 7, 4)),
    'p1={}'.format(_get_bits(val, 3, 0)),
    ]

def reset_and_misc_control_reg(val):
    return [
    'parallel_enable={}'.format(_get_bits(val, 9)),
    'oe_gp_enable={}'.format(_get_bits(val, 8)),
    'clkin_ip_pd_en={}'.format(_get_bits(val, 5)),
    'ip_pd_en={}'.format(_get_bits(val, 4)),
    'vgp_ip_pd_en={}'.format(_get_bits(val, 3)),
    'mipi_tx_reset={}'.format(_get_bits(val, 1)),
    'reset_soc_i2c={}'.format(_get_bits(val, 0)),
    ]

def second_scl_sda_pd(val):
    return ['disable secondary i2c={}'.format(val)]

def vdd_dis_counter_reg(val):
    return ['standby delay = {}/EXTCLK = {:.1f} us'.format(val, val / EXTCLK)]

def pad_slew_pad_config_reg(val):
    return [
    'slew_pxlclk={}'.format(_get_bits(val, 10, 8)),
    'slew_vgpio={}'.format(_get_bits(val, 6, 4)),
    'slew_io={}'.format(_get_bits(val, 2, 0)),
    ]

def i2c_master_frequency_divider(val):
    return ['= {}'.format(val)]

def sensor_clock_divider_reg(val):
    return [
    '(secondary sensor)',
    'clk_sensor_pll_bypass={}'.format(_get_bits(val, 10)),
    'clk_sensor1_en={}'.format(_get_bits(val, 8)),
    'clk_sensor1_divider={}'.format(_get_bits(val, 3, 0)),
    ]

def standby_control_and_status_reg(val):
    return [
    'en_irq={}'.format(_get_bits(val, 3)),
    'powerup_stop_mcu={}'.format(_get_bits(val, 2)),
    'standby_i2c={}'.format(_get_bits(val, 0)),
    ]

def i2c_master_control(val):
    return [
    'ignore_ack_err={}'.format(_get_bits(val, 1)),
    'i2cm_go={}'.format(_get_bits(val, 0)),
    ]


data = [
    {reset_and_misc_control_reg , 0x0219},
    {reset_and_misc_control_reg , 0x0018},
    (pll_control_reg  , 0x2425),
    (pll_control_reg  , 0x2145),
    (pll_dividers_reg , 0x0110),
    (pll_p_dividers_reg , 0x00f0),
    (pll_p4_p5_p6_dividers_reg , 0x7f77),
    (pll_control_reg , 0x2545),
    (pll_control_reg , 0x2547),
    (pll_control_reg , 0x3447),
    (pll_control_reg , 0x3047),
    (pll_control_reg , 0x3046),
]
data = [
            {BEEF_REG , 50 },
            {second_scl_sda_pd , 0x0001},
            {BEEF_REG , 1 },
            {second_scl_sda_pd , 0x0001},
            {BEEF_REG , 1 },
            {second_scl_sda_pd , 0x0001},
            {BEEF_REG , 1 },
            {second_scl_sda_pd , 0x0001},
            {BEEF_REG , 1 },
            {second_scl_sda_pd , 0x0001},
            {BEEF_REG , 1 },
            {second_scl_sda_pd , 0x0001},
            {BEEF_REG , 1 },
            {BEEF_REG , 10 },
]
data = [
            {vdd_dis_counter_reg , 0x01f4},
            {pad_slew_pad_config_reg , 0x0707},
            {i2c_master_frequency_divider , 0x01f4},
            {sensor_clock_divider_reg , 0x0500},
            {standby_control_and_status_reg , 0x402b},
            {i2c_master_control , 0x0004},
            {standby_control_and_status_reg , 0x402f},
            {standby_control_and_status_reg , 0x402e},
]

data = [ {standby_control_and_status_reg , 0x002a}, ]
def comment_decompile(data):
    for f, val in data:
        if type(val) != int:
            f, val = val, f
        print('            {%s , 0x%04x }, // %s' 
            % (f.__name__, val, ' '.join(f(val))))

# comment_decompile(data)

bit_info = """
...
"""

def parse_bits_info(bit_info_txt):
    lines = bit_info_txt.split('\n')
    names = []
    prev = ''
    for line in lines:
        if re.match(fourHex+'$', prev) and line != 'Reserved':
            names.append(line)
        prev = line
    print('    return [')
    for name in names:
        idx = lines.index(name)
        bits = lines[idx-2]
        print("    '{}={}'.format(_get_bits(val, {})),".format(name, '{}',  ', '.join(bits.split(':'))))
    print('    ]')
# parse_bits_info(bit_info)


def parse_bits_info_var(bit_info_txt, id_, offset):
    if bit_info_txt.strip() == '...':
        return
    lines = bit_info_txt.split('\n')
    names = []
    prev = ''
    for line in lines:
        if re.match(regHex+'{2,4}$', prev) and line != 'Reserved':
            names.append(line)
        prev = line
    print('    if id_=={} and offset=={}:'.format(id_, offset))
    print('        return [')
    for name in names:
        idx = lines.index(name)
        bits = lines[idx-2]
        print("        '{}={}'.format(_get_bits(val, {})),".format(name, '{}',  ', '.join(bits.split(':'))))
    print('        ]')
parse_bits_info_var(bit_info, 26, 7)


def PIXCLK(base=768):
    for f, t_iter in groupby(sorted( (i * j, i-1, j-1) for i in range(1,17) for j in range(i, 17) ), lambda x: x[0]):
        print('{:6.2f} MHz, /={:3}: {}'.format(
            float(base) / f, f, ' | '.join('p1={:2}, p2={:2}'.format(p1, p2) for _, p1, p2 in t_iter)
            ))


# PIXCLK()
