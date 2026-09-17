# DNS Record Analyzer 🌍

A Python-based Network Operations Center (NOC) utility for footprinting domain names and extracting critical DNS architecture configurations.

**Features:**
* Automates the retrieval of standard A (IPv4) and AAAA (IPv6) records.
* Extracts MX (Mail Exchange) records to identify organizational email routing.
* Pulls TXT records to expose domain authentication frameworks (SPF/DMARC) often utilized during SOC reconnaissance.
* Built with a robust Tkinter graphical console using the `dnspython` resolver library.

*Built as Day 8 of a 30-Day Network Engineering & Security portfolio streak.*
