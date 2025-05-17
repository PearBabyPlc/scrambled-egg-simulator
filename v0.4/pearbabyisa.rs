const SMB:f64 = 6356750.0;
const G:f64 = 9.80665;
const R:f64 = 8.3145;
const E:f64 = std::f64::consts::E;
const MOL:f64 = 0.0289644;

fn main() {
    let (mut a, mut t, mut p, mut d) = get_isa_conditions(-1000.0);
    println!("Geopotential altitude: {:?}", a);
    println!("Temperature: {:?}", t);
    println!("Pressure: {:?}", p);
    println!("Density: {:?}", d);
    println!();
    (a, t, p, d) = get_isa_conditions(15000.0);
    println!("Geopotential altitude: {:?}", a);
    println!("Temperature: {:?}", t);
    println!("Pressure: {:?}", p);
    println!("Density: {:?}", d);
    println!();
    (a, t, p, d) = get_isa_conditions(25000.0);
    println!("Geopotential altitude: {:?}", a);
    println!("Temperature: {:?}", t);
    println!("Pressure: {:?}", p);
    println!("Density: {:?}", d);
    println!();
    (a, t, p, d) = get_isa_conditions(40000.0);
    println!("Geopotential altitude: {:?}", a);
    println!("Temperature: {:?}", t);
    println!("Pressure: {:?}", p);
    println!("Density: {:?}", d);
    println!();
}

fn solve_conditions(ref_t:f64, ref_p:f64, ref_d:f64, lapse:f64, geop:f64, ref_geop:f64) -> (f64, f64, f64) {
    let temperature:f64 = ref_t - (lapse * (geop - ref_geop));
    if lapse == 0.0 {
        let p_exp:f64 = (-G * MOL * (geop - ref_geop)) / (R * ref_t);
        let pressure:f64 = ref_p * E.powf(p_exp);
        let density:f64 = ref_d * E.powf(p_exp);
        return (temperature, pressure, density)
    } else {
        let p_exp:f64 = (G * MOL) / (R * lapse);
        let pressure:f64 = ref_p * (1.0 - (lapse / ref_t)*(geop - ref_geop)).powf(p_exp);
        let d_exp:f64 = p_exp - 1.0;
        let density:f64 = ref_d * ((ref_t - (geop - ref_geop)*lapse) / ref_t).powf(d_exp);
        return (temperature, pressure, density)
    }
}
fn get_isa_conditions(alt_geom: f64) -> (f64, f64, f64, f64) {
    let alt_geop:f64 = (SMB * alt_geom) / (SMB + alt_geom);
    let mut kelvin:f64 = 0.0;
    let mut pascal:f64 = 0.0;
    let mut density:f64 = 0.0;
    if alt_geop < 11000.0 {
        (kelvin, pascal, density) = solve_conditions(288.15, 101325.0, 1.225, 0.0065, alt_geop, 0.0);
    } else if alt_geop < 20000.0 {
        (kelvin, pascal, density) = solve_conditions(216.65, 22632.1, 0.36391, 0.0, alt_geop, 11000.0);
    } else if alt_geop < 32000.0 {
        (kelvin, pascal, density) = solve_conditions(216.65, 5474.89, 0.08803, -0.001, alt_geop, 20000.0);
    } else if alt_geop < 47000.0 {
        (kelvin, pascal, density) = solve_conditions(228.65, 868.02, 0.01322, -0.0028, alt_geop, 32000.0);
    } else if alt_geop < 51000.0 {
        (kelvin, pascal, density) = solve_conditions(270.65, 110.91, 0.00143, 0.0, alt_geop, 47000.0);
    } else if alt_geop < 71000.0 {
        (kelvin, pascal, density) = solve_conditions(270.65, 66.94, 0.00086, 0.0028, alt_geop, 51000.0);
    } else if alt_geop >= 71000.0 {
        (kelvin, pascal, density) = solve_conditions(214.65, 3.96, 0.000064, 0.002, alt_geop, 71000.0);
    } else {
        println!("FAILURE WAA");
        kelvin = 0.0;
        pascal = 0.0;
        density = 0.0;
    }
    return (alt_geop, kelvin, pascal, density);
}
