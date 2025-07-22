import { Component } from '@angular/core';
import {Router, RouterLink} from '@angular/router';
import { CommonModule } from '@angular/common';
import {HttpClient, HttpClientModule} from '@angular/common/http';
import { RouterModule } from '@angular/router';
import {FormsModule} from "@angular/forms";

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule, RouterLink, FormsModule],
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css']
})
export class DashboardComponent {
  userMessage = '';
  chatMessages: { role: string, content: string }[] = [
    { role: 'bot', content: 'Hello! How can I assist you today?' }
  ];

  constructor(private http: HttpClient, private router: Router) {}

account() {
  this.router.navigate(['/account']);
}

sendMessage() {
    if (!this.userMessage.trim()) return;

    // Display user message in chat
    this.chatMessages.push({ role: 'user', content: this.userMessage });

    this.http.post<{ reply: string }>('http://localhost:8010/chat', { message: this.userMessage })
      .subscribe({
        next: (response) => {
          this.chatMessages.push({ role: 'bot', content: response.reply });
        },
        error: (err) => {
          this.chatMessages.push({ role: 'bot', content: 'Error: Could not reach AI doctor.' });
        }
      });

    this.userMessage = '';
  }



}
