# Slow Control scipts for the DUNE ND-LAr 2x2 demonstrator

Collection of existing slow control software for the DUNE ND-LAr 2x2 demonstrator experiment.

## Configuration
Configuration filename by default: "config.ini"\
To use example config file:\
`cp config_example.ini config.ini`

## Start scripts on device
Each directory (e.g. `RTD, PFD5,..`) contains two executable bash scripts:
- `start_<DEVICE>.sh` to start the readout in the current session (for debugging)
- `start_<DEVICE>_in_screen.sh` to start the readout in a detached screen session in the background

## Start scripts from remote
TO BE ADDED


## Task List
- [ ] Check Spellman scripts, update to InfluxDB v2 and implement config parser
- [ ] Write MPOD scripts
- [x] Write AIM TTi (SiPM ps input bias) scripts (see https://github.com/Planet911/tti-plp-remote/blob/master/tti-plp-remote.py)
- [ ] Include database push to TTI scripts
- [ ] Update RTD scripts to include module number
- [ ] Test RTD scripts on device
- [ ] Write general example script of how to push to InfluxDB2
- [ ] Upload/Write remote start/stop scripts
- [ ] Have a beer :beer:
