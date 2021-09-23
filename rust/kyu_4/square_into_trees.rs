fn decompose(n: i64) -> Option<Vec<i64>> {
    let mut goal = 0i64;
    let mut result = vec![n];
    while result.len() > 0 {
        let current = result.pop().unwrap();
        goal += current*current;
        for i in (0..current).rev() {
            if goal - (i*i) >= 0 {
                goal -= i*i;
                result.push(i);
                if goal == 0 {
                    result.sort();
                    return Some(result);
                }
            }
        }
    }
    None
}
