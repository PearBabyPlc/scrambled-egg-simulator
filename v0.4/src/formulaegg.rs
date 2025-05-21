use std::f64;
const THETA:f64 = 3055.0 + (5.0 / 9.0);
const E:f64 = f64::consts::E;

pub fn get_cp_r(gam_i:f64, t:f64, cp_i:f64) -> f64 {
    let theta_t = THETA / t;
    let cp_r = cp_i * (1.0 + ((gam_i - 1.0) / gam_i) *
        (theta_t.powf(2.0) * ((E.powf(theta_t)) / (E.powf(theta_t) - 1.0).powf(2.0))));
    return cp_r
}

pub fn get_gam_r(gam_i: f64, t: f64) -> f64 {
    let gam_minus = gam_i - 1.0;
    let theta_t = THETA / t;
    let gam_r = 1.0 + (gam_minus /
        (1.0 + gam_minus * (theta_t.powf(2.0) *
            (E.powf(theta_t) / (E.powf(theta_t) - 1.0).powf(2.0)))));
    return gam_r
}

pub fn get_sos(gam:f64, rs:f64, t:f64) -> f64 {
    let sos = (gam * rs * t).powf(0.5);
    return sos
}

pub fn get_stag_ratios_i(gam:f64, m:f64) -> (f64, f64, f64) {
    use std::time::Instant;
    let start = Instant::now();
    let stag_param = 1.0 + ((gam - 1.0) / 2.0) * m.powf(2.0);
    let t_st = stag_param.powf(-1.0);
    let p_sp = stag_param.powf(-gam / (gam - 1.0));
    let d_sd = stag_param.powf(-1.0 / (gam - 1.0));
    let elapsed = start.elapsed();
    println!("Ideal isentropic time: {:.2?}", elapsed);
    return (t_st, p_sp, d_sd)
}

fn stag_temp_relation(t:f64, st:f64, gam_i:f64) -> f64 {
    let msq = ((2.0 * st) / (get_gam_r(gam_i, t) * t)) *
        ((gam_i / (gam_i - 1.0)) * (1.0 - (t / st)) +
            (THETA / st) * ((1.0 / (E.powf(THETA / st) - 1.0)) -
                (1.0 / (E.powf(THETA / t) - 1.0))));
    return msq
}

fn stag_p_d_ratios(t:f64, st:f64, gam_i:f64) -> (f64, f64) {
    let theta_t = THETA / t;
    let theta_st = THETA / st;
    let t_st = t / st;
    let left = (E.powf(theta_st) - 1.0) /
        (E.powf(theta_t) - 1.0);
    let right = E.powf(theta_t * (E.powf(theta_t) / (E.powf(theta_t) - 1.0)) -
        theta_st * (E.powf(theta_st) / (E.powf(theta_st) - 1.0)));
    let d_exp = 1.0 / (gam_i - 1.0);
    let p_exp = gam_i / (gam_i - 1.0);
    let d_sd = left * t_st.powf(d_exp) * right;
    let p_sp = left * t_st.powf(p_exp) * right;
    return (d_sd, p_sp)
}

pub fn get_stag_ratios_r(gam_i:f64, m:f64, t:f64) -> (f64, f64, f64) {
    use std::time::Instant;
    let start = Instant::now();
    let st_r = t / ((1.0 + ((get_gam_r(gam_i, t) - 1.0) / 2.0) * m.powf(2.0)).powf(-1.0));
    let st_r_max = st_r * 1.01;
    let st_r_min = st_r * 0.50;
    let msq_target = m.powf(2.0);
    let mut delta_st: Vec<(f64, f64)> = Vec::new();
    let mut st_test = st_r_min;
    println!();
    while st_test <= st_r_max {
        let msq_test = stag_temp_relation(t, st_test, gam_i);
        let delta_msq = (msq_test - msq_target).abs();
        println!("st_test = {0}, m_test = {1}", st_test, msq_test.powf(0.5));
        delta_st.push((delta_msq, st_test));
        st_test += 1.0;
    }
    println!();
    delta_st.sort_by(|x, y| x.partial_cmp(y).unwrap());
    let delta_st_target = &delta_st[0];
    let st_target = delta_st_target.1;
    let (d_sd, p_sp) = stag_p_d_ratios(t, st_target, gam_i);
    let t_st = t / st_target;
    let elapsed = start.elapsed();
    println!("Mach uncertainty: ±{}", delta_st_target.0);
    println!("Real isentropic time: {:.2?}", elapsed);
    return (t_st, p_sp, d_sd)
}
