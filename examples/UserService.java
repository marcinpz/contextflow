package com.example.service;

import org.springframework.stereotype.Service;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.beans.factory.annotation.Autowired;

@Service
public class UserService {

    @Value("${app.database.url}")
    private String databaseUrl;

    @Value("${app.database.username}")
    private String dbUsername;

    @Autowired
    private UserRepository userRepository;

    @Autowired
    private EmailService emailService;

    public User findUserById(Long id) {
        // Some business logic
        return userRepository.findById(id);
    }

    public void sendWelcomeEmail(String email) {
        emailService.sendEmail(email, "Welcome!");
    }
}