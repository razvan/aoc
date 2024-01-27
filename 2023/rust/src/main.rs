mod day12;

use anyhow::{Context, Result};
use std::env;

fn main() -> Result<()> {
    let input = env::args().nth(1).context("Please supply an input")?;
    day12::run(&input)?;
    Ok(())
}
