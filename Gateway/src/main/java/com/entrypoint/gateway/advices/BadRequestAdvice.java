package com.entrypoint.gateway.advices;

import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestControllerAdvice;

import com.entrypoint.gateway.exceptions.BadRequestException;

@RestControllerAdvice
public class BadRequestAdvice {
    
    @ExceptionHandler(BadRequestException.class)
    @ResponseStatus(HttpStatus.BAD_REQUEST)
    String BadRequestHandler(BadRequestException ex) {
        return ex.getMessage();
    }
}
