import {Component, Renderer2} from '@angular/core';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent {
  inputText: string;
  hideResult = true;
  queries = Array();
  result = {text:'', profanity:'', output:[]};
  display = false;

  constructor(private renderer: Renderer2) {
    this.renderer.setStyle(document.body, 'background', 'linear-gradient(to right, #0062E6, #33AEFF)');
    this.inputText = '';
  }

  sendPostRequest(textToCheck: string) {
    const data = {text: textToCheck, key: '2167476'};

    fetch('http://95.183.140.57:8080/profanity_check', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify(data),
    }).then((response) => response.json())
      // tslint:disable-next-line:no-shadowed-variable
      .then((response) => {
        response['text'] = this.inputText;
        this.result = response;

        this.queries.push(response);
        this.hideResult = false;
        setTimeout(() => {
          this.hideResult = true;
          // this.inputText = '';
        }, 5000);
      })
      .catch((error) => {
        console.error('Error:', error);
      });
  }

  ShowResult() {
    this.sendPostRequest(this.inputText);
  }

  ngOnDestroy() {
    this.renderer.removeStyle(document.body, 'background');
  }

}
