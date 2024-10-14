package com.entrypoint.gateway.exceptions;

public class InvalidPasswordException extends RuntimeException{
    public InvalidPasswordException(String msg) {
        super(msg);
    }
}
