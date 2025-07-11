import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import numpy as np
 
# Set style for better-looking plots
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")
 
class WaferAnalyzer:
    def __init__(self, csv_file):
        """Initialize the analyzer with data from CSV file."""
        self.data = pd.read_csv(csv_file)
        self.prepare_data()
    
    def prepare_data(self):
        """Clean and prepare the data for analysis."""
        # Convert Date column to datetime
        self.data['Date'] = pd.to_datetime(self.data['Date'])
        
        # Add derived columns
        self.data['Quality_Score'] = self.data['Yield_Percentage'] - (self.data['Defect_Count'] * 2)
        self.data['Pass_Fail'] = self.data['Yield_Percentage'].apply(lambda x: 'Pass' if x >= 95 else 'Fail')
        
        # Sort by date for time series analysis
        self.data = self.data.sort_values('Date')
        
        print("Data loaded and prepared successfully!")
        print(f"Dataset shape: {self.data.shape}")
        print(f"Date range: {self.data['Date'].min()} to {self.data['Date'].max()}")
        
    def summary_statistics(self):
        """Display comprehensive summary statistics."""
        print("\n" + "="*50)
        print("SUMMARY STATISTICS")
        print("="*50)
        
        # Basic statistics
        print(f"Average Yield: {self.data['Yield_Percentage'].mean():.2f}%")
        print(f"Median Yield: {self.data['Yield_Percentage'].median():.2f}%")
        print(f"Yield Standard Deviation: {self.data['Yield_Percentage'].std():.2f}%")
        print(f"Max Defect Count: {self.data['Defect_Count'].max()}")
        print(f"Average Defect Count: {self.data['Defect_Count'].mean():.2f}")
        
        # Pass/Fail analysis
        pass_fail_counts = self.data['Pass_Fail'].value_counts()
        print(f"\nPass Rate: {pass_fail_counts.get('Pass', 0)}/{len(self.data)} ({pass_fail_counts.get('Pass', 0)/len(self.data)*100:.1f}%)")
        
        # Correlation analysis
        correlation = self.data['Yield_Percentage'].corr(self.data['Defect_Count'])
        print(f"Correlation between Yield and Defects: {correlation:.3f}")
        
        return self.data.describe()
    
    def create_visualizations(self):
        """Create comprehensive visualizations."""
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('Semiconductor Wafer Analysis Dashboard', fontsize=16, fontweight='bold')
        
        # 1. Yield vs Defects Scatter Plot
        scatter = axes[0, 0].scatter(self.data['Defect_Count'], self.data['Yield_Percentage'], 
                                   c=self.data['Quality_Score'], cmap='RdYlGn', s=100, alpha=0.7)
        axes[0, 0].set_xlabel('Defect Count')
        axes[0, 0].set_ylabel('Yield Percentage (%)')
        axes[0, 0].set_title('Yield vs Defects (colored by Quality Score)')
        axes[0, 0].grid(True, alpha=0.3)
        plt.colorbar(scatter, ax=axes[0, 0], label='Quality Score')
        
        # Add trend line
        z = np.polyfit(self.data['Defect_Count'], self.data['Yield_Percentage'], 1)
        p = np.poly1d(z)
        axes[0, 0].plot(self.data['Defect_Count'], p(self.data['Defect_Count']), 
                       "r--", alpha=0.8, linewidth=2)
        
        # 2. Time Series Analysis
        axes[0, 1].plot(self.data['Date'], self.data['Yield_Percentage'], 
                       marker='o', linewidth=2, markersize=8, label='Yield %')
        axes[0, 1].axhline(y=95, color='r', linestyle='--', alpha=0.7, label='Target (95%)')
        axes[0, 1].set_xlabel('Date')
        axes[0, 1].set_ylabel('Yield Percentage (%)')
        axes[0, 1].set_title('Yield Percentage Over Time')
        axes[0, 1].legend()
        axes[0, 1].grid(True, alpha=0.3)
        axes[0, 1].tick_params(axis='x', rotation=45)
        
        # 3. Defect Count Distribution
        axes[1, 0].hist(self.data['Defect_Count'], bins=range(int(self.data['Defect_Count'].min()), 
                                                              int(self.data['Defect_Count'].max()) + 2),
                       alpha=0.7, edgecolor='black')
        axes[1, 0].set_xlabel('Defect Count')
        axes[1, 0].set_ylabel('Frequency')
        axes[1, 0].set_title('Distribution of Defect Counts')
        axes[1, 0].grid(True, alpha=0.3)
        
        # 4. Pass/Fail Analysis
        pass_fail_counts = self.data['Pass_Fail'].value_counts()
        colors = ['#2ecc71', '#e74c3c']  # Green for Pass, Red for Fail
        wedges, texts, autotexts = axes[1, 1].pie(pass_fail_counts.values, 
                                                  labels=pass_fail_counts.index,
                                                  autopct='%1.1f%%', startangle=90,
                                                  colors=colors)
        axes[1, 1].set_title('Pass/Fail Distribution (≥95% = Pass)')
        
        plt.tight_layout()
        plt.show()
        
    def detailed_wafer_analysis(self):
        """Analyze individual wafer performance."""
        print("\n" + "="*50)
        print("INDIVIDUAL WAFER ANALYSIS")
        print("="*50)
        
        # Sort by yield percentage
        sorted_data = self.data.sort_values('Yield_Percentage', ascending=False)
        
        print("Top Performers:")
        print(sorted_data[['Wafer_ID', 'Yield_Percentage', 'Defect_Count', 'Quality_Score']].head())
        
        print("\nBottom Performers:")
        print(sorted_data[['Wafer_ID', 'Yield_Percentage', 'Defect_Count', 'Quality_Score']].tail())
        
        # Create individual wafer performance chart
        plt.figure(figsize=(12, 6))
        
        # Color code bars based on pass/fail
        colors = ['green' if x >= 95 else 'red' for x in self.data['Yield_Percentage']]
        
        bars = plt.bar(self.data['Wafer_ID'], self.data['Yield_Percentage'], color=colors, alpha=0.7)
        plt.axhline(y=95, color='black', linestyle='--', alpha=0.8, label='Target (95%)')
        plt.xlabel('Wafer ID')
        plt.ylabel('Yield Percentage (%)')
        plt.title('Individual Wafer Performance')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        # Add value labels on bars
        for bar, value in zip(bars, self.data['Yield_Percentage']):
            plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                    f'{value:.1f}%', ha='center', va='bottom', fontweight='bold')
        
        plt.tight_layout()
        plt.show()
    
    def generate_report(self):
        """Generate a comprehensive analysis report."""
        print("\n" + "="*60)
        print("COMPREHENSIVE WAFER ANALYSIS REPORT")
        print("="*60)
        
        # Data overview
        print(f"Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Total Wafers Analyzed: {len(self.data)}")
        print(f"Analysis Period: {self.data['Date'].min().strftime('%Y-%m-%d')} to {self.data['Date'].max().strftime('%Y-%m-%d')}")
        
        # Performance metrics
        avg_yield = self.data['Yield_Percentage'].mean()
        pass_rate = (self.data['Yield_Percentage'] >= 95).mean() * 100
        
        print(f"\nKEY PERFORMANCE INDICATORS:")
        print(f"• Average Yield: {avg_yield:.2f}%")
        print(f"• Pass Rate (≥95%): {pass_rate:.1f}%")
        print(f"• Average Defect Count: {self.data['Defect_Count'].mean():.2f}")
        
        # Recommendations
        print(f"\nRECOMMENDations:")
        if avg_yield < 95:
            print("• Overall yield is below target. Consider process optimization.")
        if self.data['Defect_Count'].mean() > 5:
            print("• High defect count detected. Review quality control processes.")
        if pass_rate < 80:
            print("• Low pass rate. Investigate root causes of failures.")
        
        # Identify problematic wafers
        problem_wafers = self.data[self.data['Yield_Percentage'] < 95]
        if len(problem_wafers) > 0:
            print(f"• {len(problem_wafers)} wafer(s) below target yield: {', '.join(problem_wafers['Wafer_ID'].tolist())}")

# Main execution
def main():
    """Main function to run the analysis."""
    try:
        # Initialize analyzer
        analyzer = WaferAnalyzer('wafer_data.csv')
        
        # Display first few rows
        print("First 5 rows of data:")
        print(analyzer.data.head())
        
        # Run comprehensive analysis
        analyzer.summary_statistics()
        analyzer.create_visualizations()
        analyzer.detailed_wafer_analysis()
        analyzer.generate_report()
        
    except FileNotFoundError:
        print("Error: wafer_data.csv not found. Please ensure the file exists in the current directory.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
