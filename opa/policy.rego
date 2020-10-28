
package policy

default allow = false

allow = true {
    count(violation) == 0
}

violation [user] {
    user := input.user
    user.macos <= 10.13
}

violation [user] {
    user := input.user
    user.chromeos <= 80.15
}
