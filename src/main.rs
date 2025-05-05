mod watcher;
mod git_ops;

use std::env;

fn main() {
    let repo_path = env::current_dir().expect("Failed to get current directory");
    watcher::start_watching(repo_path);
}
