time cargo build --release --features sqlite 
strip -s target/release/vaultwarden
time cargo generate-rpm && ls -l target/generate-rpm/vaultwarden*.rpm && rpm -qlp target/generate-rpm/vaultwarden*.rpm 

