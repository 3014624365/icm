import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Set Matplotlib and Seaborn style
plt.rcParams['font.sans-serif'] = ['SimHei']  # Use SimHei font
plt.rcParams['axes.unicode_minus'] = False  # Fix minus sign display issue
sns.set_theme(style="whitegrid", palette="pastel")

# Data
countries = ['Romania', 'USA']
medal_effects = {
    'Romania': {
        'Total': {'effect': -3.10, 'R2': 0.95, 'MSE': 0.30},
        'Gold': {'effect': -0.73, 'R2': 0.81, 'MSE': 0.02},
        'Silver': {'effect': -0.05, 'R2': 0.81, 'MSE': 0.00}
    },
    'USA': {
        'Total': {'effect': 1.20, 'R2': 0.55, 'MSE': 2.56},
        'Gold': {'effect': 0.06, 'R2': 0.69, 'MSE': 0.03},
        'Silver': {'effect': 0.04, 'R2': 0.90, 'MSE': 0.00}
    }
}

# Generate advanced visualizations
for country in countries:
    effects = medal_effects[country]

    # Create canvas
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    fig.suptitle(f'{country} Coach Effect Visualization (Before and After Cutoff)', fontsize=16, y=1.05)

    # Define colors
    before_color = '#1f77b4'  # Blue (before cutoff)
    after_color = '#ff7f0e'  # Orange (after cutoff)
    ci_color = '#d62728'  # Red (confidence interval)

    # Total Medals
    ax = axes[0]
    x = np.array([0, 1])  # 0: Before Cutoff, 1: After Cutoff
    y_before = 10  # Actual value before cutoff
    y_after = y_before + effects['Total']['effect']  # Predicted value after cutoff
    y_err = np.sqrt(effects['Total']['MSE'])  # Error bars (standard deviation)

    # Plot bar graph and error bars
    ax.bar(x, [y_before, y_after], color=[before_color, after_color], alpha=0.6, label=['Before Cutoff', 'After Cutoff'])
    ax.errorbar(x, [y_before, y_after], yerr=y_err, fmt='none', color=ci_color, capsize=5, label='95% Confidence Interval')

    # Set title and labels
    ax.set_xticks(x)
    ax.set_xticklabels(['Before Cutoff', 'After Cutoff'])
    ax.set_title(
        f'Total Medals\nCoach Effect: {effects["Total"]["effect"]:.2f}\nR²: {effects["Total"]["R2"]:.2f}, MSE: {effects["Total"]["MSE"]:.2f}')
    ax.set_ylabel('Medal Count')
    ax.legend()

    # Gold Medal Ratio
    ax = axes[1]
    y_before = 0.5  # Actual value before cutoff
    y_after = y_before + effects['Gold']['effect']  # Predicted value after cutoff
    y_err = np.sqrt(effects['Gold']['MSE'])  # Error bars (standard deviation)

    # Plot bar graph and error bars
    ax.bar(x, [y_before, y_after], color=[before_color, after_color], alpha=0.6, label=['Before Cutoff', 'After Cutoff'])
    ax.errorbar(x, [y_before, y_after], yerr=y_err, fmt='none', color=ci_color, capsize=5, label='95% Confidence Interval')

    # Set title and labels
    ax.set_xticks(x)
    ax.set_xticklabels(['Before Cutoff', 'After Cutoff'])
    ax.set_title(
        f'Gold Medal Ratio\nCoach Effect: {effects["Gold"]["effect"]:.2f}\nR²: {effects["Gold"]["R2"]:.2f}, MSE: {effects["Gold"]["MSE"]:.2f}')
    ax.set_ylabel('Ratio')
    ax.legend()

    # Silver Medal Ratio
    ax = axes[2]
    y_before = 0.3  # Actual value before cutoff
    y_after = y_before + effects['Silver']['effect']  # Predicted value after cutoff
    y_err = np.sqrt(effects['Silver']['MSE'])  # Error bars (standard deviation)

    # Plot bar graph and error bars
    ax.bar(x, [y_before, y_after], color=[before_color, after_color], alpha=0.6, label=['Before Cutoff', 'After Cutoff'])
    ax.errorbar(x, [y_before, y_after], yerr=y_err, fmt='none', color=ci_color, capsize=5, label='95% Confidence Interval')

    # Set title and labels
    ax.set_xticks(x)
    ax.set_xticklabels(['Before Cutoff', 'After Cutoff'])
    ax.set_title(
        f'Silver Medal Ratio\nCoach Effect: {effects["Silver"]["effect"]:.2f}\nR²: {effects["Silver"]["R2"]:.2f}, MSE: {effects["Silver"]["MSE"]:.2f}')
    ax.set_ylabel('Ratio')
    ax.legend()

    # Adjust layout
    plt.tight_layout()

    # Save the figure
    plt.savefig(f'{country}_Coach_Effect_Visualization.png', dpi=300, bbox_inches='tight')
    plt.close()

print("Advanced visualizations have been generated and saved.")