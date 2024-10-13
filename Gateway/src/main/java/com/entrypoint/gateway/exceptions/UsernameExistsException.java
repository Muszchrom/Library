package com.entrypoint.gateway.exceptions;

public class UsernameExistsException extends RuntimeException{
    public UsernameExistsException(String msg) {
        super(msg);
    }
}
