from flask import Flask
from flask_cors import CORS

from blueprints import (
    apply_to_device, create_access_code, download_as_csv, get_co2_details,
    get_current_stats, get_led_panel, get_recipe_components, get_recipe_details,
    get_temp_details, get_user_devices, post_to_twitter, get_recipe_by_uuid,
    register_device, get_all_recipes, get_device_types, submit_recipe,
    get_plant_types, save_recipe, submit_recipe_change, verify_user_session,
    user_authenticate, upload_images, get_user_info, get_device_peripherals,
post_to_discourse,discourse_forum,
    submit_access_code,get_current_recipe, get_device_images,submit_horticulture_measurements,
    get_current_recipe_info, save_recipe_for_later,apply_recipe_to_device,save_user_profile_changes,get_current_device_status,submit_access_chamber,get_device_recipe_history,daily_horticulture_measurements,get_horticulture_daily_logs
)

app = Flask(__name__)
app.register_blueprint(apply_to_device.apply_to_device_bp)
app.register_blueprint(create_access_code.create_new_code_bp)
app.register_blueprint(download_as_csv.download_as_csv_bp)
app.register_blueprint(get_co2_details.get_co2_details_bp)
app.register_blueprint(get_current_stats.get_current_stats_bp)
app.register_blueprint(get_led_panel.get_led_panel_bp)
app.register_blueprint(get_recipe_components.get_recipe_components_bp)
app.register_blueprint(get_recipe_details.get_recipe_details_bp)
app.register_blueprint(get_temp_details.get_temp_details_bp)
app.register_blueprint(get_user_devices.get_user_devices_bp)
app.register_blueprint(post_to_twitter.posttwitter_bp)
app.register_blueprint(register_device.register_bp)
app.register_blueprint(save_recipe.save_recipe_bp)
app.register_blueprint(submit_recipe_change.submit_recipe_change_bp)
app.register_blueprint(user_authenticate.user_authenticate)
app.register_blueprint(verify_user_session.verify_user_session_bp)
app.register_blueprint(get_device_peripherals.get_device_peripherals_bp)
app.register_blueprint(submit_recipe.submit_recipe_bp)
app.register_blueprint(get_device_types.get_device_types_bp)
app.register_blueprint(get_plant_types.get_plant_types_bp)
app.register_blueprint(get_all_recipes.get_all_recipes_bp)
app.register_blueprint(get_recipe_by_uuid.get_recipe_by_uuid_bp)
app.register_blueprint(get_current_recipe_info.get_current_recipe_info_bp)
app.register_blueprint(save_recipe_for_later.save_for_later_bp)

app.register_blueprint(upload_images.upload_images_bp)
app.register_blueprint(get_user_info.get_user_info_bp)
app.register_blueprint(submit_access_code.submit_access_code_bp)
app.register_blueprint(get_device_images.get_device_images_bp)
app.register_blueprint(get_current_recipe.get_current_recipe_bp)
app.register_blueprint(apply_recipe_to_device.apply_recipe_to_device_bp)
app.register_blueprint(save_user_profile_changes.save_user_profile_bp)
app.register_blueprint(get_device_recipe_history.get_device_recipe_history_bp)
app.register_blueprint(get_current_device_status.get_current_device_status_bp)
app.register_blueprint(submit_horticulture_measurements.submit_horticulture_measurements_bp)
app.register_blueprint(submit_access_chamber.submit_access_chamber_bp)
app.register_blueprint(post_to_discourse.postdiscourse_bp)
app.register_blueprint(daily_horticulture_measurements.daily_horticulture_measurements_bp)
app.register_blueprint(get_horticulture_daily_logs.get_horticulture_daily_logs_bp)
app.register_blueprint(discourse_forum.forum_bp)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
CORS(app)

# ------------------------------------------------------------------------------
if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    app.run(host='127.0.0.1', port=5000, debug=True, threaded=True)
