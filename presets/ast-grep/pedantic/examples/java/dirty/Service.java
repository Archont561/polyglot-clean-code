// Package dirty shows the shapes PCC-S01 and PCC-S07 reject in Java.
package dirty;

final class Service {
    void start(int port) {
        System.out.println("starting");
        System.err.println("port " + port);
    }

    void stop(Exception error) {
        try {
            close();
        } catch (RuntimeException failure) {
        }
        error.printStackTrace();
    }

    private void close() {
        throw new IllegalStateException("already closed");
    }
}
