use itertools::Itertools;
use std::{
    collections::HashSet,
    env, fs,
    io::{self, BufRead},
};

use anyhow::{Context, Result};

pub fn run() -> Result<()> {
    let input = env::args().nth(1).context("Please supply an input")?;

    let file = fs::File::open(input).context("Could not open input file {input}")?;
    let mut reader = io::BufReader::new(file);
    let puzzle = parse_puzzle(&mut reader)?;

    let mut result = 0;

    for (line, groups) in puzzle.springs.iter().zip(puzzle.groups.iter()) {
        for candidate in gen(line, groups.iter().sum()) {
            if is_line_valid(&candidate, groups) {
                result += 1;
            }
        }
    }

    println!("Part 1: {}", result);

    Ok(())
}

#[derive(Debug)]
struct Puzzle {
    springs: Vec<String>,
    groups: Vec<Vec<usize>>,
}

fn parse_puzzle<R: BufRead>(reader: &mut R) -> Result<Puzzle> {
    let mut springs = vec![];
    let mut groups = vec![];

    for line in reader.lines() {
        match line {
            Ok(line) => {
                let parts: Vec<&str> = line.split(' ').collect();
                if parts.len() != 2 {
                    return Err(anyhow::anyhow!("Invalid line: {}", line));
                } else {
                    springs.push(parts[0].into());

                    let line_groups: Result<Vec<usize>, _> =
                        parts[1].split(',').map(|s| s.parse::<usize>()).collect();
                    match line_groups {
                        Ok(line_groups) => {
                            groups.push(line_groups);
                        }
                        Err(_) => {
                            return Err(anyhow::anyhow!("Cannot parse group on line {}", line));
                        }
                    }
                }
            }
            Err(_) => {
                return Err(anyhow::anyhow!("Failed to read line"));
            }
        };
    }
    Ok(Puzzle { springs, groups })
}

fn gen(line: &str, springs: usize) -> Vec<String> {
    let existing_springs = line.chars().filter(|c| *c == '#').count();
    let missing_springs = springs - existing_springs;

    let qindex: HashSet<usize> = line
        .chars()
        .enumerate()
        .filter(|(_, c)| *c == '?')
        .map(|(i, _)| i)
        .collect();

    if qindex.is_empty() {
        return vec![line.into()];
    }

    let mut result = vec![];

    for mask in qindex.into_iter().combinations(missing_springs) {
        let candidate = line
            .chars()
            .enumerate()
            .map(|(i, c)| {
                if c == '?' {
                    if mask.contains(&i) {
                        '#'
                    } else {
                        '.'
                    }
                } else {
                    c
                }
            })
            .collect::<String>();
        result.push(candidate);
    }

    result
}

fn is_line_valid(line: &str, groups: &[usize]) -> bool {
    let mut line_groups = vec![];

    let mut i = 0;
    for c in line.chars() {
        if c == '#' {
            i += 1;
        } else if i > 0 {
            line_groups.push(i);
            i = 0;
        }
    }

    if i > 0 {
        line_groups.push(i);
    }

    line_groups == groups
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_parse_puzzle() {
        let input = "???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1";
        let mut reader = io::BufReader::new(input.as_bytes());
        let puzzle = parse_puzzle(&mut reader).expect("Could not parse puzzle");

        assert_eq!(puzzle.springs.len(), 6);
        assert_eq!(puzzle.groups.len(), 6);
    }

    #[test]
    fn test_gen() {
        let line = "??.#";
        let springs = 2;
        let result = gen(line, springs);
        assert_eq!(result.len(), 2);
        assert!(result.contains(&"#..#".into()));
        assert!(result.contains(&".#.#".into()));
    }

    #[test]
    fn test_is_valid() {
        assert!(is_line_valid(".#.###.#.######", &[1, 3, 1, 6]));
    }
}
