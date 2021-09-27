mod preloaded;
use preloaded::MORSE_CODE;
// MORSE_CODE is `HashMap<String, String>`. e.g. ".-" -> "A".

pub fn decode_bits(encoded: &str) -> String {
    let stripped = encoded.trim_matches('0');
    for multiple in (1..10).rev() {
        if stripped.len() % multiple == 0 {
            let bits = stripped.chars()
                .map(|c| c.to_digit(10).unwrap())
                .collect::<Vec<_>>();
            if bits.chunks(multiple)
                .all(|chunk| chunk.iter().min() == chunk.iter().max()) {
                return stripped.chars()
                    .step_by(multiple)
                    .collect::<String>();
            }
        }
    }
    unreachable!()
}

pub fn decode_morse(encoded: &str) -> String {
    let decoded = encoded
        .replace("000", " ")
        .replace("111", "-")
        .replace("1", ".")
        .replace("0", "");
    
    decoded.split(" ")
        .map(|s| s.to_string())
        .map(|s| MORSE_CODE.get(&s).unwrap_or(&" ".to_string()).to_string())
        .collect::<String>()
}
