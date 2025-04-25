import matplotlib.pyplot as plt

################################################################################

def plot_nivel(df, local):
    fig, ax = plt.subplots()
    ax.set_title(f"Nível do Rio, {local}")
    ax.set_ylabel("Nível do rio")
    ax.set_xlabel("Data")
    ax.plot(df['Data'], df['Cotas'])
    return fig

def plot_chuva(df, local):
    fig, ax = plt.subplots()
    ax.set_title(f"Chuvas, {local}")
    ax.set_ylabel("Chuvas")
    ax.set_xlabel("Data")
    ax.bar(df['Data'], df['Cotas'], color='purple')
    return fig
