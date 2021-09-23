fn dbl_linear(n: u32) -> u32{
    let mut u = vec![1u32];
    let mut yi = 0;
    let mut zi = 0;
    for _ in 0..n {
        let y_next = 2*u[yi] + 1;
        let z_next = 3*u[zi] + 1;
        if y_next <= z_next {
            u.push(y_next);
            yi += 1;
            if y_next == z_next {
                zi += 1;
            }
        } else {
            u.push(z_next);
            zi += 1;
        }
    }
    u[n as usize]
}
