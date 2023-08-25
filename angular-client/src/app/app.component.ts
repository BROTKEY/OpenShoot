import { Component, ElementRef, OnInit, ViewChild } from '@angular/core';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss'],
})
export class AppComponent implements OnInit {
  @ViewChild('canvas', { static: true }) canvas!: ElementRef<HTMLCanvasElement>;
  context!: CanvasRenderingContext2D;
  // all | serie | shot | data
  series: number[][][][] = [[[]]];
  socket = new WebSocket('ws://localhost:8000');
  calibratedTriggerPull: number = 5000;
  trigger_samples = 0;
  trigger_calibrated = false;
  startTime = new Date().getTime();
  trigger_pull_time = 0;
  shot_selected = false;

  ngOnInit(): void {
    this.context = this.canvas.nativeElement.getContext('2d')!;
    const img = new Image();
    img.src = 'assets/Luftgewehrscheibe.png';
    img.onload = () => {
      this.context.drawImage(img, 0, 0);
      this.context.beginPath();
    };

    //retrive current time in ms

    this.socket.onmessage = (event) => {
      const receivedTime = new Date().getTime();

      const data = event.data.split(';');
      const shotdata = [
        ((parseFloat(data[0]) * -1) / 3) * 271 + 400,
        ((parseFloat(data[1]) * -1) / 3) * 271 + 400,
        parseFloat(data[2]),
      ];
      if (this.trigger_samples < 1000 && shotdata[2] > 0) {
        this.calibratedTriggerPull =
          shotdata[2] < this.calibratedTriggerPull
            ? shotdata[2]
            : this.calibratedTriggerPull;
        this.trigger_samples++;
        if (this.trigger_samples == 1000) {
          this.trigger_calibrated = true;
        }
        return;
      }

      if (receivedTime - this.trigger_pull_time < 2000) {
        this.startTime = receivedTime;
        let series_offset = 1;
        if (this.series[this.series.length - 1].length == 1) {
          series_offset = 2;
        }

        this.series[this.series.length - series_offset][
          this.series[this.series.length - series_offset].length - 2
        ].push(shotdata);
      }

      if (receivedTime - this.trigger_pull_time < 30000) {
        return;
      }

      console.log('ping');

      if (this.series[this.series.length - 1].length > 9) {
        this.series.push([]);
      }

      if (receivedTime - this.startTime > 20000) {
        this.series[this.series.length - 1][
          this.series[this.series.length - 1].length - 1
        ] = [];
        this.startTime = receivedTime;
        return;
      }

      this.startTime = receivedTime;
      this.series[this.series.length - 1][
        this.series[this.series.length - 1].length - 1
      ].push(shotdata);

      this.detectTriggerPull(shotdata[2], receivedTime);

      if (this.shot_selected) return;

      this.selectShot(
        this.series.length - 1,
        this.series[this.series.length - 1].length - 1
      );
    };
  }

  detectTriggerPull(triggerData: number, receivedTime: number) {
    console.log(triggerData);
    console.log(this.calibratedTriggerPull);
    if (triggerData < this.calibratedTriggerPull - 40) {
      this.trigger_pull_time = receivedTime;
      console.log('PENG');
      this.series[this.series.length - 1].push([]);
      if (this.series[this.series.length - 1].length > 9) {
        this.series.push([[]]);
      }
    }
  }

  selectShot(series: number, shot: number) {
    this.context.strokeStyle = 'red';
    const img = new Image();
    img.src = 'assets/Luftgewehrscheibe.png';
    img.onload = () => {
      this.context.beginPath();
      this.context.clearRect(
        0,
        0,
        this.canvas.nativeElement.width,
        this.canvas.nativeElement.height
      );
      this.context.drawImage(img, 0, 0);
      this.series[series][shot].forEach((data, i) => {
        this.context.moveTo(data[0], data[1]);
        if (i != 0) {
          this.context.lineTo(
            this.series[series][shot][i - 1][0],
            this.series[series][shot][i - 1][1]
          );
        }
        if (!this.series[series][shot][i + 1]) {
          this.context.arc(data[0], data[1], 10, 0, 2 * Math.PI, false);
        }
      });
      this.context.stroke();
    };
  }
}
