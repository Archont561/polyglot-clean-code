// Package dirty shows the shape PCC-S01 rejects in Go.
package dirty

import "fmt"

// Start reports a service start through debug printing.
func Start(port int) {
	fmt.Println("starting")
	fmt.Printf("port %d\n", port)
}
