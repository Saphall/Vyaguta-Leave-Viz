# Insights

![Streamlit](https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ7_90yUni3jBuNFSiaJkwNs8SDbHX2t_3uAg&s)

Frontend Setup for the Leave Vizualization system.

```bash
insights/
├── .streamlit/                      # Configuration folder for Streamlit
│   └── config.toml                  # Config file for the Streamlit
├── page/                            # Different pages in Visualization app
│   ├── 1_home.py                    # Home page for the app
│   ├── 2_overview.py                # Overview dashboard page for the app
│   ├── 3_employee.py                # Employe dashboard page for the app
│   ├── 4_leave_trend.py             # Leave trend dashboard page for the app
│   └── 5_about.py                   # About page for the app
├── utils/                           # Utility codes
├── app.py                           # Main file for the frontend
├── README.md
```

## Run locally

```zsh
streamlit run insights/app.py reload
```

## Using Docker

```bash
docker compose up -d frontend
```

## Visualizations

1. **Home Page**

    ![image](https://github.com/user-attachments/assets/22db667b-0fc0-48ce-8e67-609cb32a3f6d)

    ---

2. **Customizable Visualization Options**

    | ![image](https://github.com/user-attachments/assets/dfd8fb7d-7e9a-4448-9956-4b72c3de01f8) | ![image](https://github.com/user-attachments/assets/9ae91f98-83fb-4232-bf60-39aff80f414a) | ![image](https://github.com/user-attachments/assets/cf975b66-fdf6-4675-aced-e4601eebdeea) |
    |:-----------------------------------------------------------------------------------------:|:-----------------------------------------------------------------------------------------:|:-----------------------------------------------------------------------------------------:|

3. **Overview Page**

    | ![image](https://github.com/user-attachments/assets/f84de04a-11c9-42f9-8f5c-ba9a08639922) | ![image](https://github.com/user-attachments/assets/39dbe512-f42f-421c-b45c-203d6e7c9f15) |
    |:-----------------------------------------------------------------------------------------:|:-----------------------------------------------------------------------------------------:|
    | ![image](https://github.com/user-attachments/assets/4d10e3f3-0d60-42dc-9ae2-b27924cfb7a9) | ![image](https://github.com/user-attachments/assets/783ccdbc-c594-49c6-a13b-ef12d04f959f) |

    ---

4. **Employee Page**

    | ![image](https://github.com/user-attachments/assets/bcfab445-c259-4948-9c1f-740206b53902) | ![image](https://github.com/user-attachments/assets/9a8daad7-4957-435f-8f4b-353c73fe0245) |
    |:-----------------------------------------------------------------------------------------:|:-----------------------------------------------------------------------------------------:|

5. **Leave Trends Page**

    | ![image](https://github.com/user-attachments/assets/8f21ddf5-5867-4b65-91b6-ba6592b3e5b4) | ![image](https://github.com/user-attachments/assets/964a8448-140b-40b1-b16f-4dd796fe7c07) |
    |:-----------------------------------------------------------------------------------------:|:-----------------------------------------------------------------------------------------:|
