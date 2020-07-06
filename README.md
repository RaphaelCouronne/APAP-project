
README

* Create a smtp choosing either:
    * A local server : sudo python -m smtpd -n -c DebuggingServer localhost:25
    * A remote server : (e.g. gmail / outlook...)
    * Do not forger to change `open_smtp()` accordingly

* Run main.py
    * Select customers according to given criteria
    * Send them a personalized mail
