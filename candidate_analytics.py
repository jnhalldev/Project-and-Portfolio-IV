import sys
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QLabel
from PyQt5.QtChart import QChart, QChartView, QLineSeries, QValueAxis
from PyQt5.QtGui import QPainter
from PyQt5.QtCore import Qt, QPointF
import numpy as np  # For calculating statistics, ensure you have numpy installed

class CandidateAnalyticsWindow(QMainWindow):
    def __init__(self, scores, parent=None):
        super().__init__(parent)
        self.scores = self.extract_scores(scores)
        self.scores.sort()
        self.setupUI()
        self.calculateStatistics()
        self.setupChart()

    def extract_scores(self, evaluations):
        # Extract numeric score values from each evaluation dictionary
        return [evaluation['score'] for evaluation in evaluations if 'score' in evaluation and isinstance(evaluation['score'], (int, float))]

    def setupUI(self):
        self.setWindowTitle("Candidate Analytics")
        self.setFixedSize(800, 600)

        layout = QVBoxLayout()

        # Labels for displaying statistics
        self.averageScoreLabel = QLabel("Average Score: Calculating...")
        layout.addWidget(self.averageScoreLabel)

        self.medianScoreLabel = QLabel("Median Score: Calculating...")
        layout.addWidget(self.medianScoreLabel)

        self.maxScoreLabel = QLabel("Max Score: Calculating...")
        layout.addWidget(self.maxScoreLabel)

        self.minScoreLabel = QLabel("Min Score: Calculating...")
        layout.addWidget(self.minScoreLabel)

        self.countLabel = QLabel("Number of Results: Calculating...")
        layout.addWidget(self.countLabel)

        self.chartView = QChartView()
        layout.addWidget(self.chartView)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def calculateStatistics(self):
        if self.scores:
            self.averageScoreLabel.setText(f"Average Score: {np.mean(self.scores):.2f}")
            self.medianScoreLabel.setText(f"Median Score: {np.median(self.scores):.2f}")
            self.maxScoreLabel.setText(f"Max Score: {np.max(self.scores):.2f}")
            self.minScoreLabel.setText(f"Min Score: {np.min(self.scores):.2f}")
            self.countLabel.setText(f"Number of Results: {len(self.scores)}")
        else:
            self.averageScoreLabel.setText("Average Score: N/A")
            self.medianScoreLabel.setText("Median Score: N/A")
            self.maxScoreLabel.setText("Max Score: N/A")
            self.minScoreLabel.setText("Min Score: N/A")
            self.countLabel.setText("Number of Results: N/A")

    def setupChart(self):
        chart = QChart()
        chart.setTitle("Candidate Scores")
        chart.setAnimationOptions(QChart.SeriesAnimations)

        series = QLineSeries()
        for i, score in enumerate(self.scores):
            series.append(QPointF(i, score))

        chart.addSeries(series)

        axisX = QValueAxis()
        axisX.setLabelFormat("%d")
        axisX.setTitleText("Candidates")
        chart.addAxis(axisX, Qt.AlignBottom)
        series.attachAxis(axisX)

        axisY = QValueAxis()
        axisY.setLabelFormat("%.2f")
        axisY.setTitleText("Scores")
        chart.addAxis(axisY, Qt.AlignLeft)
        series.attachAxis(axisY)

        self.chartView.setChart(chart)
        self.chartView.setRenderHint(QPainter.Antialiasing)
        