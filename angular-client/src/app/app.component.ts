import { Component, ElementRef, OnInit, ViewChild } from '@angular/core';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})

export class AppComponent implements OnInit  {
  @ViewChild('canvas', { static: true }) canvas!: ElementRef<HTMLCanvasElement>;
  context !: CanvasRenderingContext2D;
  series = [[[],[]],[[],[]]]

  ngOnInit(): void {
    this.context = this.canvas.nativeElement.getContext('2d')!; 
    const img = new Image();
    img.src = "assets/Luftgewehrscheibe_dark.png";
    img.onload = () => {this.context.drawImage(img,0,0); this.context.beginPath();};
  }

  selectShot(shot: number) { }
}
