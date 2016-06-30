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
#define second_scl_sda_pd_reg 0x0614
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
    return ['delay()'.format(val)]


def var(n):
    vartype = "VAR"
    if n & 0x8000:
        n ^= 0x8000
        vartype = "VAR8"
    print("{}({}, {})".format(vartype, n >> 10, n & ((1 << 10) - 1)))



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


# print translate(to_translate)
# pll_dividers_reg(0x0110)

def comment_decompile():
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

    for f, val in data:
        if type(val) != int:
            f, val = val, f
        print('            {%s , 0x%04x }, // %s' 
            % (f.__name__, val, ' '.join(f(val))))

comment_decompile()

bit_info = """
[ left out ]
"""

def parse_bits_info(bit_info_txt):
    lines = bit_info_txt.split('\n')
    names = []
    prev = ''
    for line in lines:
        if re.match('0x\d{4}$', prev) and line != 'Reserved':
            names.append(line)
        prev = line
    for name in names:
        idx = lines.index(name)
        bits = lines[idx-2]
        print("    '{}={}'.format(_get_bits(val, {})),".format(name, '{}',  ', '.join(bits.split(':'))))


# parse_bits_info(bit_info)

def PIXCLK(base=768):
    for f, t_iter in groupby(sorted( (i * j, i-1, j-1) for i in range(1,17) for j in range(i, 17) ), lambda x: x[0]):
        print('{:6.2f} MHz, /={:3}: {}'.format(
            float(base) / f, f, ' | '.join('p1={:2}, p2={:2}'.format(p1, p2) for _, p1, p2 in t_iter)
            ))


# PIXCLK()
