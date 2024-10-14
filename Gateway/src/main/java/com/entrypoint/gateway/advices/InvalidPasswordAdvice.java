package com.entrypoint.gateway.advices;

import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestControllerAdvice;

import com.entrypoint.gateway.exceptions.InvalidPasswordException;

@RestControllerAdvice
public class InvalidPasswordAdvice {
  
  @ExceptionHandler(InvalidPasswordException.class)
  @ResponseStatus(HttpStatus.BAD_REQUEST)
  String InvalidPasswordHandler(InvalidPasswordException ex) {
    return ex.getMessage();
  }
}