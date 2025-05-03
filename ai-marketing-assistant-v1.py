import streamlit as st
import openai
import qrcode
from PIL import Image
import io

# Initialize OpenAI API
openai.api_key = "your-openai-api-key"  # Replace with your OpenAI API key

# Streamlit app configuration
st.set_page_config(page_title="AI Marketing Assistant", page_icon="📈", layout="wide")

# App header
st.title("AI Advertising Writer + Business Marketing Checklist")
st.markdown("Generate tailored ad copy, social media posts, email campaigns, and QR codes for your small business. Follow our marketing checklist to stay on track!")

# Sidebar for industry selection and navigation
st.sidebar.header("Settings")
industry = st.sidebar.selectbox("Select Your Industry", ["Construction", "Retail", "Restaurant", "Other"])
business_name = st.sidebar.text_input("Your Business Name", "My Business")
campaign_url = st.sidebar.text_input("Campaign URL (for QR Code)", "https://example.com")

# Tabs for different functionalities
tab1, tab2, tab3, tab4 = st.tabs(["AI Content Generator", "Marketing Checklist", "QR Code Generator", "Analytics Dashboard"])

# Tab 1: AI Content Generator
with tab1:
    st.header("AI-Powered Content Generator")
    content_type = st.selectbox("Choose Content Type", ["Ad Copy", "Social Media Post", "Email Campaign"])
    tone = st.selectbox("Select Tone", ["Professional", "Casual", "Persuasive", "Friendly"])
    generate_button = st.button("Generate Content")

    if generate_button:
        # Define industry-specific prompts
        prompts = {
            "Construction": {
                "Ad Copy": f"Write a {tone.lower()} ad copy for a construction business called {business_name}. Highlight quality craftsmanship and reliability.",
                "Social Media Post": f"Create a {tone.lower()} social media post for {business_name}, a construction company. Promote a new project or service.",
                "Email Campaign": f"Draft a {tone.lower()} email campaign for {business_name}, a construction business, offering a discount on home renovations."
            },
            "Retail": {
                "Ad Copy": f"Write a {tone.lower()} ad copy for a retail store called {business_name}. Emphasize unique products and special offers.",
                "Social Media Post": f"Create a {tone.lower()} social media post for {business_name}, a retail store. Showcase a new product or sale.",
                "Email Campaign": f"Draft a {tone.lower()} email campaign for {business_name}, a retail store, promoting a seasonal sale."
            },
            "Restaurant": {
                "Ad Copy": f"Write a {tone.lower()} ad copy for a restaurant called {business_name}. Highlight signature dishes and ambiance.",
                "Social Media Post": f"Create a {tone.lower()} social media post for {business_name}, a restaurant. Promote a special menu or event.",
                "Email Campaign": f"Draft a {tone.lower()} email campaign for {business_name}, a restaurant, inviting customers to a new menu launch."
            },
            "Other": {
                "Ad Copy": f"Write a {tone.lower()} ad copy for a business called {business_name}. Focus on unique value propositions.",
                "Social Media Post": f"Create a {tone.lower()} social media post for {business_name}. Highlight a product, service, or event.",
                "Email Campaign": f"Draft a {tone.lower()} email campaign for {business_name}, promoting a new offering or event."
            }
        }

        # Generate content using OpenAI
        try:
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=prompts[industry][content_type],
                max_tokens=200,
                temperature=0.7
            )
            content = response.choices[0].text.strip()
            st.subheader("Generated Content")
            st.write(content)
            st.download_button("Download Content", content, f"{content_type.lower()}.txt")
        except Exception as e:
            st.error(f"Error generating content: {str(e)}")

# Tab 2: Marketing Checklist
with tab2:
    st.header("Business Marketing Checklist")
    st.markdown("Follow these actionable steps to boost your marketing efforts:")
    checklist = [
        ("Define your target audience", False),
        ("Set clear campaign goals (e.g., increase sales by 10%)", False),
        ("Create a content calendar for social media", False),
        ("Design and distribute campaign materials (e.g., flyers, QR codes)", False),
        ("Integrate Google Analytics to track performance", False),
        ("Analyze campaign results and adjust strategies", False)
    ]

    # Display checklist with checkboxes
    for i, (task, _) in enumerate(checklist):
        checklist[i] = (task, st.checkbox(task, key=f"check_{i}"))

    # Progress bar
    completed = sum(1 for _, checked in checklist if checked)
    progress = completed / len(checklist)
    st.progress(progress)
    st.write(f"Progress: {completed}/{len(checklist)} tasks completed")

# Tab 3: QR Code Generator
with tab3:
    st.header("QR Code Generator")
    if st.button("Generate QR Code"):
        if campaign_url:
            # Generate QR code
            qr = qrcode.QRCode(version=1, box_size=10, border=4)
            qr.add_data(campaign_url)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")

            # Save QR code to bytes for download
            buf = io.BytesIO()
            img.save(buf, format="PNG")
            byte_im = buf.getvalue()

            # Display QR code
            st.image(img, caption="Your Campaign QR Code", use_column_width=False)

            # Download button
            st.download_button("Download QR Code", byte_im, "qrcode.png", "image/png")
        else:
            st.error("Please enter a valid campaign URL in the sidebar.")

# Tab 4: Analytics Dashboard (Placeholder)
with tab4:
    st.header("Analytics Dashboard")
    st.markdown("Connect your Google Analytics account to track campaign performance.")
    st.info("Analytics integration is under development. For now, manually check your Google Analytics dashboard for insights.")
    # Placeholder for future integration
    st.write("Example Metrics (Coming Soon):")
    st.write("- Campaign Impressions")
    st.write("- Click-Through Rate (CTR)")
    st.write("- Conversion Rate")

# Footer
st.markdown("---")
st.markdown("Built with ❤️ by xAI | For support, contact support@x.ai")
