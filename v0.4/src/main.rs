use crate::formulaegg as egg;
use crate::pearbabyisa as isa;
mod formulaegg;
mod pearbabyisa;

fn main() {
    //let (alt_geop, t, p, d) = isa::get_isa_conditions(38000.0);
    //println!("Geopotential altitude: {}m", alt_geop);
    let t = 3800.0;
    let p = 100000.0 * 25.0;
    let d = 12.8;
    let gam_i = 1.4;
    let cp_i = 1005.0;
    let gam_r = egg::get_gam_r(gam_i, t);
    let cp_r = egg::get_cp_r(gam_i, t, cp_i);
    println!("Gamma = {}", gam_r);
    println!("Cp = {}", cp_r);
    let rs = 287.0;
    let sos = egg::get_sos(gam_r, rs, t);
    println!("SoS = {}", sos);
    let m0 = 3.0;
    println!("QUASI ISENTROPIC RELATIONS");
    let (mut t_st, mut p_sp, mut d_sd) = egg::get_stag_ratios_i(gam_r, m0);
    let mut st = t / t_st;
    let mut sp = p / p_sp;
    let mut sd = d / d_sd;
    println!("Stag T = {}", st);
    println!("Stag P = {}", sp);
    println!("Stag D = {}", sd);
    println!();
    println!("REAL ISENTROPIC RELATIONS");
    (t_st, p_sp, d_sd) = egg::get_stag_ratios_r(gam_i, m0, t);
    st = t / t_st;
    sp = p / p_sp;
    sd = d / d_sd;
    println!("Stag T = {}", st);
    println!("Stag P = {}", sp);
    println!("Stag D = {}", sd);
}
