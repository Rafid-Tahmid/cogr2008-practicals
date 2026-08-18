JAVAC ?= javac
JAVA ?= java
JFLAGS ?= -g

.PHONY: all run clean

all: SharedAccount.class SharedAccountClient.class DriverATM.class

SharedAccount.class: SharedAccount.java
	$(JAVAC) $(JFLAGS) SharedAccount.java

SharedAccountClient.class: SharedAccountClient.java SharedAccount.class
	$(JAVAC) $(JFLAGS) SharedAccountClient.java

DriverATM.class: DriverATM.java SharedAccount.class SharedAccountClient.class
	$(JAVAC) $(JFLAGS) DriverATM.java

run: all
	$(JAVA) DriverATM

clean:
	rm -f *.class
