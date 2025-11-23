from manim import *

class CombinedVideo(Scene):
    """
    Machine Learning Complete Course
    Multi-scene video with 8 parts
    
    Total Duration: 110.0 seconds
    Number of Scenes: 8
    """
    
    def construct(self):
        """Main video construction with multiple scenes."""
        # Title card
        title = Text("Machine Learning Complete Course", font_size=48)
        self.play(Write(title))
        self.wait(1)
        self.play(FadeOut(title))
        
        # Play all scenes in sequence
        self.scene_1()
        self.scene_2()
        self.scene_3()
        self.scene_4()
        self.scene_5()
        self.scene_6()
        self.scene_7()
        self.scene_8()
        
        # End card
        end_text = Text("End", font_size=36)
        self.play(FadeIn(end_text))
        self.wait(1)

    def scene_1(self):
        """Scene 1: Introduction to Machine Learning"""
        # Clear previous scene
        self.clear()
        
        # Scene content
                self.camera.background_color = BLACK

                # Create objects
                title_ml = Text("Machine Learning", color=BLUE, font_size=1.2 * DEFAULT_FONT_SIZE)
                title_ml.move_to([0, 3.5, 0])

                subtitle_definition = Text("Automating analytical model building from data.", color=WHITE, font_size=0.7 * DEFAULT_FONT_SIZE)
                subtitle_definition.move_to([0, 2, 0])

                bullet_learns_data = Text("• Learns from data", color=GREEN, font_size=0.6 * DEFAULT_FONT_SIZE)
                bullet_learns_data.move_to([-4, 0.5, 0])

                bullet_identifies_patterns = Text("• Identifies patterns", color=GREEN, font_size=0.6 * DEFAULT_FONT_SIZE)
                bullet_identifies_patterns.move_to([-4, -0.5, 0])

                bullet_makes_decisions = Text("• Makes decisions", color=GREEN, font_size=0.6 * DEFAULT_FONT_SIZE)
                bullet_makes_decisions.move_to([-4, -1.5, 0])

                bullet_minimal_intervention = Text("• Minimal human intervention", color=GREEN, font_size=0.6 * DEFAULT_FONT_SIZE)
                bullet_minimal_intervention.move_to([-4, -2.5, 0])

                # Animation Timeline
                # anim_create_title (start_time: 0.0, duration: 1.0)
                self.play(Create(title_ml), run_time=1.0)

                # anim_write_subtitle (start_time: 1.0, duration: 2.0)
                # Current time: 1.0. Next animation starts at 1.0. No wait needed.
                self.play(Write(subtitle_definition), run_time=2.0)

                # anim_fade_in_learns_data (start_time: 3.5, duration: 0.8)
                # Current time: 1.0 + 2.0 = 3.0. Next animation starts at 3.5. Wait for 0.5s.
                self.wait(0.5)
                self.play(FadeIn(bullet_learns_data), run_time=0.8)

                # anim_fade_in_identifies_patterns (start_time: 4.5, duration: 0.8)
                # Current time: 3.5 + 0.8 = 4.3. Next animation starts at 4.5. Wait for 0.2s.
                self.wait(0.2)
                self.play(FadeIn(bullet_identifies_patterns), run_time=0.8)

                # anim_fade_in_makes_decisions (start_time: 5.5, duration: 0.8)
                # Current time: 4.5 + 0.8 = 5.3. Next animation starts at 5.5. Wait for 0.2s.
                self.wait(0.2)
                self.play(FadeIn(bullet_makes_decisions), run_time=0.8)

                # anim_fade_in_minimal_intervention (start_time: 6.5, duration: 0.8)
                # Current time: 5.5 + 0.8 = 6.3. Next animation starts at 6.5. Wait for 0.2s.
                self.wait(0.2)
                self.play(FadeIn(bullet_minimal_intervention), run_time=0.8)

                # Current time: 6.5 + 0.8 = 7.3. Remaining wait: 10.0 - 7.3 = 2.7s.
                self.wait(2.7)
        
        # Scene transition
        self.wait(0.5)
    def scene_2(self):
        """Scene 2: Supervised Learning Explained"""
        # Clear previous scene
        self.clear()
        
        # Scene content
                self.camera.background_color = BLACK

                # Create objects
                title_supervised_learning = Text("Supervised Learning Explained")
                title_supervised_learning.move_to([0, 3.0, 0])
                title_supervised_learning.set_color(WHITE)
                title_supervised_learning.scale(1.2)
                title_supervised_learning.set_opacity(1.0)
        
                def_part1 = Text(
                    "Supervised learning is a machine learning task where a function learns to map input to output based on example input-output pairs.",
                    disable_ligatures=True
                )
                def_part1.move_to([-4.0, 1.5, 0])
                def_part1.set_color(WHITE)
                def_part1.scale(0.7)
                def_part1.set_opacity(1.0)
        
                def_part2 = Text(
                    "It infers a function from labeled training data.",
                    disable_ligatures=True
                )
                def_part2.move_to([-4.0, 0.7, 0])
                def_part2.set_color(WHITE)
                def_part2.scale(0.7)
                def_part2.set_opacity(1.0)
        
                goal_text = Text(
                    "The goal is to approximate this mapping function so well that it can predict output variables for new input data.",
                    disable_ligatures=True
                )
                goal_text.move_to([-4.0, -0.5, 0])
                goal_text.set_color(WHITE)
                goal_text.scale(0.7)
                goal_text.set_opacity(1.0)
        
                algorithms_list = Text(
                    "Common algorithms include: Linear Regression, Logistic Regression, Decision Trees, Random Forests, and Support Vector Machines.",
                    disable_ligatures=True
                )
                algorithms_list.move_to([-4.0, -2.0, 0])
                algorithms_list.set_color(WHITE)
                algorithms_list.scale(0.7)
                algorithms_list.set_opacity(1.0)

                # Animate with proper timing
                # anim_create_title (start_time: 0.0, duration: 1.0)
                self.play(Create(title_supervised_learning), run_time=1.0)
        
                # anim_write_def1 (delay: 0.5, duration: 3.0)
                self.wait(0.5)
                self.play(Write(def_part1), run_time=3.0)
        
                # anim_write_def2 (delay: 0.5, duration: 2.0)
                self.wait(0.5)
                self.play(Write(def_part2), run_time=2.0)
        
                # anim_write_goal (delay: 0.5, duration: 3.0)
                self.wait(0.5)
                self.play(Write(goal_text), run_time=3.0)
        
                # anim_write_algorithms (delay: 0.5, duration: 4.0)
                self.wait(0.5)
                self.play(Write(algorithms_list), run_time=4.0)
        
                # Total duration of animations and waits:
                # 1.0 (title) + 0.5 (wait) + 3.0 (def1) + 0.5 (wait) + 2.0 (def2) + 0.5 (wait) + 3.0 (goal) + 0.5 (wait) + 4.0 (algo) = 15.0 seconds
                self.wait() # A small default wait at the end
        
        # Scene transition
        self.wait(0.5)
    def scene_3(self):
        """Scene 3: Unsupervised Learning Explained"""
        # Clear previous scene
        self.clear()
        
        # Scene content
                self.camera.background_color = BLACK

                # Create objects
                scene_title = Text("Unsupervised Learning Explained")
                scene_title.move_to([0, 3.5, 0])
                scene_title.set_color(BLUE)

                definition_text = Text(
                    "Unsupervised learning is a type of machine learning that looks for previously undetected patterns in a data set with no pre-existing labels and minimal human supervision.",
                    font_size=30,  # Adjust font size to fit
                    line_spacing=1.5
                )
                definition_text.move_to([0, 1.5, 0])
                definition_text.set_color(WHITE)

                techniques_header = Text("Common techniques:")
                techniques_header.move_to([-3, -0.5, 0])
                techniques_header.set_color(YELLOW)

                technique1_text = Text("• Clustering")
                technique1_text.move_to([-2, -1.5, 0])
                technique1_text.set_color(GREEN)

                technique2_text = Text("• Association Rule Learning")
                technique2_text.move_to([-2, -2.0, 0])
                technique2_text.set_color(GREEN)

                technique3_text = Text("• Dimensionality Reduction")
                technique3_text.move_to([-2, -2.5, 0])
                technique3_text.set_color(GREEN)

                kmeans_desc = Text(
                    "K-means clustering groups data points into clusters based on similarity.",
                    font_size=25, # Adjust font size to fit
                    line_spacing=1.2
                )
                kmeans_desc.move_to([2.5, -1.5, 0])
                kmeans_desc.set_color(WHITE)

                pca_desc = Text(
                    "Principal Component Analysis (PCA) reduces data dimensionality while preserving important information.",
                    font_size=25, # Adjust font size to fit
                    line_spacing=1.2
                )
                pca_desc.move_to([2.5, -2.5, 0])
                pca_desc.set_color(WHITE)

                # Animate with proper timing
                # anim_title_create
                self.wait(0.0) # Delay from previous (none)
                self.play(Create(scene_title), run_time=1.5)

                # anim_definition_write
                self.wait(0.5) # Delay from previous animation's end
                self.play(Write(definition_text), run_time=3.0)

                # anim_kmeans_desc_write
                self.wait(0.3) # Delay from previous animation's end
                self.play(Write(kmeans_desc), run_time=2.0)

                # anim_pca_desc_write
                self.wait(0.3) # Delay from previous animation's end
                self.play(Write(pca_desc), run_time=2.0)

                # anim_techniques_header_fade_in
                self.wait(0.5) # Delay from previous animation's end
                self.play(FadeIn(techniques_header), run_time=1.0)

                # anim_technique1_fade_in
                self.wait(0.3) # Delay from previous animation's end
                self.play(FadeIn(technique1_text), run_time=1.0)

                # anim_technique2_fade_in
                self.wait(0.3) # Delay from previous animation's end
                self.play(FadeIn(technique2_text), run_time=1.0)

                # anim_technique3_fade_in
                self.wait(0.3) # Delay from previous animation's end
                self.play(FadeIn(technique3_text), run_time=1.0)

                # The total duration of the scene is 15.0s.
                # The sum of run_times and waits:
                # 1.5 (title) + 0.5 (wait) + 3.0 (def) + 0.3 (wait) + 2.0 (kmeans) + 0.3 (wait) + 2.0 (pca) + 0.5 (wait) + 1.0 (header) + 0.3 (wait) + 1.0 (tech1) + 0.3 (wait) + 1.0 (tech2) + 0.3 (wait) + 1.0 (tech3) = 15.0
                # No final self.wait() is needed as the last animation ends exactly at 15.0s.
        
        # Scene transition
        self.wait(0.5)
    def scene_4(self):
        """Scene 4: Understanding Neural Networks"""
        # Clear previous scene
        self.clear()
        
        # Scene content
                self.camera.background_color = BLACK

                # --- Create Objects ---
                # Text Objects
                main_title = Text("Understanding Neural Networks", font_size=0.8 * 40)
                main_title.move_to([0, 3.5, 0])
                main_title.set_color(WHITE)

                part_info = Text("Part 4 of 8", font_size=0.5 * 40)
                part_info.move_to([-6, 3.5, 0])
                part_info.set_color(GREY)

                nn_intro_text = Text("A neural network recognizes underlying relationships in data.", font_size=0.6 * 40)
                nn_intro_text.move_to([0, 0, 0])
                nn_intro_text.set_color(WHITE)

                input_label = Text("Input Layer", font_size=0.5 * 40)
                input_label.move_to([-4, 2.5, 0])
                input_label.set_color(WHITE)

                hidden_label = Text("Hidden Layers", font_size=0.5 * 40)
                hidden_label.move_to([0, 3, 0])
                hidden_label.set_color(WHITE)

                output_label = Text("Output Layer", font_size=0.5 * 40)
                output_label.move_to([4, 1.5, 0])
                output_label.set_color(WHITE)

                weights_text = Text("Each connection has a weight.", font_size=0.5 * 40)
                weights_text.move_to([0, -3.5, 0])
                weights_text.set_color(YELLOW)

                activation_text = Text("Activation functions determine neuron activity.", font_size=0.5 * 40)
                activation_text.move_to([0, -3.5, 0])
                activation_text.set_color(GREEN)

                # Node Objects (Circles)
                node_radius = 0.4 # A suitable radius for the nodes
                input_node_1 = Circle(radius=node_radius).move_to([-4, 1.5, 0]).set_color(BLUE).set_opacity(1.0)
                input_node_2 = Circle(radius=node_radius).move_to([-4, 0, 0]).set_color(BLUE).set_opacity(1.0)
                input_node_3 = Circle(radius=node_radius).move_to([-4, -1.5, 0]).set_color(BLUE).set_opacity(1.0)

                hidden_node_1 = Circle(radius=node_radius).move_to([0, 2, 0]).set_color(BLUE).set_opacity(1.0)
                hidden_node_2 = Circle(radius=node_radius).move_to([0, 0.7, 0]).set_color(BLUE).set_opacity(1.0)
                hidden_node_3 = Circle(radius=node_radius).move_to([0, -0.7, 0]).set_color(BLUE).set_opacity(1.0)
                hidden_node_4 = Circle(radius=node_radius).move_to([0, -2, 0]).set_color(BLUE).set_opacity(1.0)

                output_node_1 = Circle(radius=node_radius).move_to([4, 0.7, 0]).set_color(BLUE).set_opacity(1.0)
                output_node_2 = Circle(radius=node_radius).move_to([4, -0.7, 0]).set_color(BLUE).set_opacity(1.0)

                # Group all nodes for easier animation
                all_nodes = VGroup(
                    input_node_1, input_node_2, input_node_3,
                    hidden_node_1, hidden_node_2, hidden_node_3, hidden_node_4,
                    output_node_1, output_node_2
                )

                # Line Objects (Connections) - defined after nodes to get their centers
                # Input Layer to Hidden Layer connections
                line_i1_h1 = Line(input_node_1.get_center(), hidden_node_1.get_center()).set_color(GREY).set_opacity(1.0)
                line_i1_h2 = Line(input_node_1.get_center(), hidden_node_2.get_center()).set_color(GREY).set_opacity(1.0)
                line_i1_h3 = Line(input_node_1.get_center(), hidden_node_3.get_center()).set_color(GREY).set_opacity(1.0)
                line_i1_h4 = Line(input_node_1.get_center(), hidden_node_4.get_center()).set_color(GREY).set_opacity(1.0)

                line_i2_h1 = Line(input_node_2.get_center(), hidden_node_1.get_center()).set_color(GREY).set_opacity(1.0)
                line_i2_h2 = Line(input_node_2.get_center(), hidden_node_2.get_center()).set_color(GREY).set_opacity(1.0)
                line_i2_h3 = Line(input_node_2.get_center(), hidden_node_3.get_center()).set_color(GREY).set_opacity(1.0)
                line_i2_h4 = Line(input_node_2.get_center(), hidden_node_4.get_center()).set_color(GREY).set_opacity(1.0)

                line_i3_h1 = Line(input_node_3.get_center(), hidden_node_1.get_center()).set_color(GREY).set_opacity(1.0)
                line_i3_h2 = Line(input_node_3.get_center(), hidden_node_2.get_center()).set_color(GREY).set_opacity(1.0)
                line_i3_h3 = Line(input_node_3.get_center(), hidden_node_3.get_center()).set_color(GREY).set_opacity(1.0)
                line_i3_h4 = Line(input_node_3.get_center(), hidden_node_4.get_center()).set_color(GREY).set_opacity(1.0)

                # Hidden Layer to Output Layer connections
                line_h1_o1 = Line(hidden_node_1.get_center(), output_node_1.get_center()).set_color(GREY).set_opacity(1.0)
                line_h1_o2 = Line(hidden_node_1.get_center(), output_node_2.get_center()).set_color(GREY).set_opacity(1.0)

                line_h2_o1 = Line(hidden_node_2.get_center(), output_node_1.get_center()).set_color(GREY).set_opacity(1.0)
                line_h2_o2 = Line(hidden_node_2.get_center(), output_node_2.get_center()).set_color(GREY).set_opacity(1.0)

                line_h3_o1 = Line(hidden_node_3.get_center(), output_node_1.get_center()).set_color(GREY).set_opacity(1.0)
                line_h3_o2 = Line(hidden_node_3.get_center(), output_node_2.get_center()).set_color(GREY).set_opacity(1.0)

                line_h4_o1 = Line(hidden_node_4.get_center(), output_node_1.get_center()).set_color(GREY).set_opacity(1.0)
                line_h4_o2 = Line(hidden_node_4.get_center(), output_node_2.get_center()).set_color(GREY).set_opacity(1.0)

                # Group lines for easier animation
                input_to_hidden_lines = VGroup(
                    line_i1_h1, line_i1_h2, line_i1_h3, line_i1_h4,
                    line_i2_h1, line_i2_h2, line_i2_h3, line_i2_h4,
                    line_i3_h1, line_i3_h2, line_i3_h3, line_i3_h4
                )
                hidden_to_output_lines = VGroup(
                    line_h1_o1, line_h1_o2,
                    line_h2_o1, line_h2_o2,
                    line_h3_o1, line_h3_o2,
                    line_h4_o1, line_h4_o2
                )
                all_lines = VGroup(input_to_hidden_lines, hidden_to_output_lines)

                # --- Animations ---
                # Initialize current time for precise timing
                current_time = 0.0

                # anim_title_part_create (start_time: 0.0, duration: 0.5)
                self.play(Create(main_title), Create(part_info), run_time=0.5)
                current_time = 0.5

                # anim_nn_intro_write (start_time: 0.7, duration: 2.0)
                self.wait(0.7 - current_time)
                self.play(Write(nn_intro_text), run_time=2.0)
                current_time = 0.7 + 2.0

                # anim_nn_intro_fade_out (start_time: 2.7, duration: 0.5)
                self.wait(2.7 - current_time) # This should be 0 wait
                self.play(FadeOut(nn_intro_text), run_time=0.5)
                current_time = 2.7 + 0.5

                # anim_nodes_create (start_time: 3.5, duration: 1.0)
                self.wait(3.5 - current_time)
                self.play(Create(all_nodes), run_time=1.0)
                current_time = 3.5 + 1.0

                # anim_labels_write (start_time: 4.5, duration: 0.5)
                self.wait(4.5 - current_time)
                self.play(Write(input_label), Write(hidden_label), Write(output_label), run_time=0.5)
                current_time = 4.5 + 0.5

                # anim_connections_draw_ih (start_time: 5.0, duration: 1.0)
                self.wait(5.0 - current_time)
                self.play(ShowCreation(input_to_hidden_lines), run_time=1.0)
                current_time = 5.0 + 1.0

                # anim_connections_draw_ho (start_time: 6.0, duration: 1.0)
                self.wait(6.0 - current_time)
                self.play(ShowCreation(hidden_to_output_lines), run_time=1.0)
                current_time = 6.0 + 1.0

                # anim_weights_text_fade_in (start_time: 7.0, duration: 0.5)
                # anim_connections_indicate_weights (start_time: 7.0, duration: 1.0)
                self.wait(7.0 - current_time)
                self.play(
                    FadeIn(weights_text, run_time=0.5),
                    Indicate(all_lines, run_time=1.0)
                )
                current_time = 7.0 + max(0.5, 1.0) # Advance by the max duration of parallel animations

                # anim_weights_text_fade_out (start_time: 8.0, duration: 0.5)
                self.wait(8.0 - current_time)
                self.play(FadeOut(weights_text), run_time=0.5)
                current_time = 8.0 + 0.5

                # anim_activation_text_fade_in (start_time: 8.5, duration: 0.5)
                # anim_nodes_indicate_activation (start_time: 8.5, duration: 1.0)
                self.wait(8.5 - current_time)
                self.play(
                    FadeIn(activation_text, run_time=0.5),
                    Indicate(all_nodes, run_time=1.0)
                )
                current_time = 8.5 + max(0.5, 1.0) # Advance by the max duration of parallel animations

                # anim_activation_text_fade_out (start_time: 9.5, duration: 0.5)
                self.wait(9.5 - current_time)
                self.play(FadeOut(activation_text), run_time=0.5)
                current_time = 9.5 + 0.5

                # Final wait to ensure the scene lasts the specified duration or for comfortable viewing
                # The last animation ends exactly at 10.0s. Add a small buffer wait.
                self.wait(0.5)
        
        # Scene transition
        self.wait(0.5)
    def scene_5(self):
        """Scene 5: Introduction to Deep Learning"""
        # Clear previous scene
        self.clear()
        
        # Scene content
                self.camera.background_color = BLACK

                # Object mapping dictionary to store Manim objects by their IDs
                obj_map = {}

                # Create objects
                title_dl = Text("Deep Learning", color=BLUE).scale(1.2).move_to([0, 3.5, 0])
                obj_map["title_dl"] = title_dl

                definition = Text("A subset of machine learning based on artificial neural networks with representation learning.", color=WHITE).scale(0.7).move_to([0, 2.0, 0])
                obj_map["definition"] = definition

                architectures_header = Text("Architectures:", color=YELLOW).scale(0.8).move_to([-4.0, 0.5, 0])
                obj_map["architectures_header"] = architectures_header

                dnn = Text("- Deep Neural Networks (DNNs)", color=WHITE).scale(0.6).move_to([-3.0, -0.5, 0])
                obj_map["dnn"] = dnn

                rnn = Text("- Recurrent Neural Networks (RNNs)", color=WHITE).scale(0.6).move_to([-3.0, -1.2, 0])
                obj_map["rnn"] = rnn

                cnn_arch = Text("- Convolutional Neural Networks (CNNs)", color=WHITE).scale(0.6).move_to([-3.0, -1.9, 0])
                obj_map["cnn_arch"] = cnn_arch

                applications_header = Text("Applications:", color=YELLOW).scale(0.8).move_to([3.0, 0.5, 0])
                obj_map["applications_header"] = applications_header

                comp_vision = Text("- Computer Vision", color=WHITE).scale(0.6).move_to([4.0, -0.5, 0])
                obj_map["comp_vision"] = comp_vision

                nlp = Text("- Natural Language Processing", color=WHITE).scale(0.6).move_to([4.0, -1.2, 0])
                obj_map["nlp"] = nlp

                speech_rec = Text("- Speech Recognition", color=WHITE).scale(0.6).move_to([4.0, -1.9, 0])
                obj_map["speech_rec"] = speech_rec

                cnn_note = Text("CNNs are particularly effective for Image Recognition tasks.", color=GREEN).scale(0.7).move_to([0, -3.0, 0])
                obj_map["cnn_note"] = cnn_note

                # Animation Timeline data
                timeline_data = [
                  {"start_time": -3.0, "animation_id": "anim_7", "animation_type": "fade_in", "targets": ["applications_header"], "duration": 0.7},
                  {"start_time": 0.0, "animation_id": "anim_1", "animation_type": "write", "targets": ["title_dl"], "duration": 1.0},
                  {"start_time": 0.3, "animation_id": "anim_4", "animation_type": "write", "targets": ["dnn"], "duration": 1.0},
                  {"start_time": 0.3, "animation_id": "anim_5", "animation_type": "write", "targets": ["rnn"], "duration": 1.0},
                  {"start_time": 0.3, "animation_id": "anim_6", "animation_type": "write", "targets": ["cnn_arch"], "duration": 1.0},
                  {"start_time": 0.3, "animation_id": "anim_8", "animation_type": "write", "targets": ["comp_vision"], "duration": 1.0},
                  {"start_time": 0.3, "animation_id": "anim_9", "animation_type": "write", "targets": ["nlp"], "duration": 1.0},
                  {"start_time": 0.3, "animation_id": "anim_10", "animation_type": "write", "targets": ["speech_rec"], "duration": 1.0},
                  {"start_time": 0.5, "animation_id": "anim_2", "animation_type": "write", "targets": ["definition"], "duration": 2.5},
                  {"start_time": 0.5, "animation_id": "anim_3", "animation_type": "fade_in", "targets": ["architectures_header"], "duration": 0.7},
                  {"start_time": 0.5, "animation_id": "anim_11", "animation_type": "write", "targets": ["cnn_note"], "duration": 2.5}
                ]

                # Sort timeline by start_time to process chronologically
                timeline_data.sort(key=lambda x: x["start_time"])

                # Calculate time offset to ensure all animations start at non-negative times
                min_start_time = 0.0
                if timeline_data:
                    min_start_time = timeline_data[0]["start_time"]
        
                time_offset = -min_start_time if min_start_time < 0 else 0.0

                # Group animations by their adjusted start time
                animations_at_time = {}
                for entry in timeline_data:
                    adjusted_start_time = entry["start_time"] + time_offset
            
                    # Assuming single target for all given animations
                    target_mobject = obj_map[entry["targets"][0]]
            
                    manim_anim = None
                    if entry["animation_type"] == "write":
                        manim_anim = Write(target_mobject, run_time=entry["duration"])
                    elif entry["animation_type"] == "fade_in":
                        manim_anim = FadeIn(target_mobject, run_time=entry["duration"])
            
                    if manim_anim:
                        if adjusted_start_time not in animations_at_time:
                            animations_at_time[adjusted_start_time] = []
                        animations_at_time[adjusted_start_time].append(manim_anim)
        
                # Get sorted list of unique adjusted start times
                sorted_adjusted_start_times = sorted(animations_at_time.keys())

                # Process animations sequentially by their adjusted start times
                for start_time_block in sorted_adjusted_start_times:
                    # Wait until this block's start time.
                    # Use max(0, ...) to handle cases where current self.time might be ahead
                    # (due to previous animations finishing later than the next scheduled start).
                    # This ensures valid non-negative wait times, though it might serialize
                    # some animations that were intended to overlap in the original timeline.
                    wait_duration = start_time_block - self.time
                    if wait_duration > 0:
                        self.wait(wait_duration)
            
                    # Play all animations scheduled for this start time concurrently
                    animations_to_play = animations_at_time[start_time_block]
                    self.play(*animations_to_play)
        
                total_scene_duration_original = 15.0
                # If the original content duration is 15.0s and the earliest start time was -3.0s,
                # it means the content effectively runs from -3.0s to 12.0s (relative to original 0).
                # After shifting by +3.0s, the content runs from 0.0s to 15.0s (relative to adjusted 0).
                # So, the target end time for the adjusted timeline is 15.0s.
                target_end_time_adjusted = total_scene_duration_original 

                if self.time < target_end_time_adjusted:
                    self.wait(target_end_time_adjusted - self.time)
        
        # Scene transition
        self.wait(0.5)
    def scene_6(self):
        """Scene 6: Evaluating Machine Learning Models"""
        # Clear previous scene
        self.clear()
        
        # Scene content
                self.camera.background_color = BLACK

                # Create objects
                scene_title = Text("Evaluating Machine Learning Models")
                scene_title.move_to([0, 3, 0])
                scene_title.set_color(WHITE)

                # For long texts, adjust font_size and max_width for better readability and wrapping
                eval_definition = Text(
                    "Model evaluation is the process of using different metrics to understand a machine learning model's performance, strengths, and weaknesses.",
                    font_size=28,
                    line_spacing=1.2,
                    max_width=10 # Ensures text wraps within a reasonable width
                )
                # Adjust position slightly if max_width changes the effective center
                eval_definition.move_to([-0.5, 1.5, 0]) 
                eval_definition.set_color(LIGHT_GRAY)

                metrics_header = Text("Common metrics include:")
                metrics_header.move_to([-4, 0, 0])
                metrics_header.set_color(WHITE)

                metrics_list = Text("accuracy, precision, recall, F1-score, and ROC curves.")
                metrics_list.move_to([-3, -0.7, 0])
                metrics_list.set_color(YELLOW)

                cv_header = Text("Cross-validation:")
                cv_header.move_to([-4, -2, 0])
                cv_header.set_color(WHITE)

                cv_definition = Text(
                    "a technique used to assess how well a model will generalize to an independent dataset, involving partitioning data into subsets for training and validation.",
                    font_size=28,
                    line_spacing=1.2,
                    max_width=10 # Ensures text wraps within a reasonable width
                )
                # Adjust position slightly if max_width changes the effective center
                cv_definition.move_to([-0.5, -3, 0])
                cv_definition.set_color(LIGHT_GRAY)

                # Animations (using LaggedStart for parallel animations with specific start times)
                animations_to_run = []
                lag_times = []
                max_animation_end_time = 0.0

                # anim_title (start_time: 0.0, duration: 1.5)
                animations_to_run.append(Write(scene_title).set_run_time(1.5))
                lag_times.append(0.0)
                max_animation_end_time = max(max_animation_end_time, 0.0 + 1.5)

                # anim_metrics_list (start_time: 0.3, duration: 2.5)
                animations_to_run.append(Write(metrics_list).set_run_time(2.5))
                lag_times.append(0.3)
                max_animation_end_time = max(max_animation_end_time, 0.3 + 2.5)

                # anim_cv_def (start_time: 0.3, duration: 3.5)
                animations_to_run.append(Write(cv_definition).set_run_time(3.5))
                lag_times.append(0.3)
                max_animation_end_time = max(max_animation_end_time, 0.3 + 3.5)

                # anim_eval_def (start_time: 0.5, duration: 3.0)
                animations_to_run.append(Write(eval_definition).set_run_time(3.0))
                lag_times.append(0.5)
                max_animation_end_time = max(max_animation_end_time, 0.5 + 3.0)

                # anim_metrics_header (start_time: 0.5, duration: 1.5)
                animations_to_run.append(Write(metrics_header).set_run_time(1.5))
                lag_times.append(0.5)
                max_animation_end_time = max(max_animation_end_time, 0.5 + 1.5)

                # anim_cv_header (start_time: 0.5, duration: 1.5)
                animations_to_run.append(Write(cv_header).set_run_time(1.5))
                lag_times.append(0.5)
                max_animation_end_time = max(max_animation_end_time, 0.5 + 1.5)

                # Play all animations in parallel with specified lags
                # The run_time of LaggedStart is determined by the latest ending animation
                self.play(
                    LaggedStart(*animations_to_run, lag_times=lag_times),
                    run_time=max_animation_end_time
                )

                # Calculate remaining time after all animations in LaggedStart have finished.
                remaining_time = 15.0 - max_animation_end_time
                if remaining_time > 0:
                    self.wait(remaining_time)
                else:
                    # Ensure at least a small wait if calculations result in 0 or negative
                    self.wait(1.0)
        
        # Scene transition
        self.wait(0.5)
    def scene_7(self):
        """Scene 7: Overfitting and Regularization"""
        # Clear previous scene
        self.clear()
        
        # Scene content
                self.camera.background_color = BLACK

                # Create objects
                title_text = Text(
                    "Overfitting and Regularization",
                    color=WHITE,
                    font_size=1.0 * 15, # Manim's Text font_size is scaled by 15 by default
                ).move_to([0, 3.2, 0])

                overfitting_def = Text(
                    "Overfitting: Model learns training data too well, including noise,\nleading to poor generalization.",
                    color=WHITE,
                    font_size=0.6 * 15,
                    line_spacing=1.2
                ).move_to([-4, 1.5, 0]).set_x(0).align_to(LEFT, direction=LEFT) # Align to left after centering

                regularization_def = Text(
                    "Regularization: Prevents overfitting by adding a penalty term\nto the loss function.",
                    color=WHITE,
                    font_size=0.6 * 15,
                    line_spacing=1.2
                ).move_to([-4, 0.0, 0]).set_x(0).align_to(LEFT, direction=LEFT)

                techniques_header = Text(
                    "Common Techniques:",
                    color=YELLOW,
                    font_size=0.7 * 15,
                ).move_to([-4, -1.5, 0]).set_x(0).align_to(LEFT, direction=LEFT)

                l1_lasso = Text(
                    "- L1 Regularization (Lasso)",
                    color=BLUE,
                    font_size=0.5 * 15,
                ).move_to([-3.5, -2.2, 0]).set_x(0).align_to(LEFT, direction=LEFT)

                l2_ridge = Text(
                    "- L2 Regularization (Ridge)",
                    color=BLUE,
                    font_size=0.5 * 15,
                ).move_to([-3.5, -2.7, 0]).set_x(0).align_to(LEFT, direction=LEFT)

                dropout = Text(
                    "- Dropout (Neural Networks)",
                    color=BLUE,
                    font_size=0.5 * 15,
                ).move_to([-3.5, -3.2, 0]).set_x(0).align_to(LEFT, direction=LEFT)

                early_stopping = Text(
                    "- Early Stopping",
                    color=BLUE,
                    font_size=0.5 * 15,
                ).move_to([-3.5, -3.7, 0]).set_x(0).align_to(LEFT, direction=LEFT)

                # Animate with proper timing
                self.play(Create(title_text), run_time=1.0)
                # Delay 0.0s (anim_overfitting_def starts at 1.0, title_text ends at 1.0)
                self.play(Write(overfitting_def), run_time=3.0)
                self.wait(0.5) # Delay 4.5 - 4.0 = 0.5s
                self.play(Write(regularization_def), run_time=3.0)
                self.wait(0.5) # Delay 8.0 - 7.5 = 0.5s
                self.play(Create(techniques_header), run_time=1.0)
                self.wait(0.5) # Delay 9.5 - 9.0 = 0.5s
                self.play(Write(l1_lasso), run_time=1.5)
                # Delay 0.0s (anim_l2_ridge starts at 11.0, l1_lasso ends at 11.0)
                self.play(Write(l2_ridge), run_time=1.5)
                # Delay 0.0s (anim_dropout starts at 12.5, l2_ridge ends at 12.5)
                self.play(Write(dropout), run_time=1.5)
                # Delay 0.0s (anim_early_stopping starts at 14.0, dropout ends at 14.0)
                self.play(Write(early_stopping), run_time=1.5)
                self.wait(2.5) # Final wait for total duration 18.0s (18.0 - 15.5 = 2.5s)
        
        # Scene transition
        self.wait(0.5)
    def scene_8(self):
        """Scene 8: The Art of Feature Engineering"""
        # Clear previous scene
        self.clear()
        
        # Scene content
                self.camera.background_color = BLACK

                # Create objects
                part_series_text = Text("Part 8 of 8").move_to([-4.0, 3.5, 0]).set_color(GREY).scale(0.6)
                title_text = Text("The Art of Feature Engineering").move_to([0, 2.5, 0]).set_color(YELLOW).scale(1.2)
                definition_text_1 = Text("Feature engineering is selecting, modifying, or creating features").move_to([0, 0.5, 0]).set_color(WHITE).scale(0.8)
                definition_text_2 = Text("to improve machine learning model performance.").move_to([0, -0.5, 0]).set_color(GREEN).scale(0.8)
                techniques_title = Text("Key Techniques:").move_to([-3.0, -1.5, 0]).set_color(BLUE).scale(0.7)
                technique_1 = Text("- Feature Selection").move_to([-2.5, -2.0, 0]).set_color(WHITE).scale(0.6)
                technique_2 = Text("- Feature Extraction").move_to([-2.5, -2.5, 0]).set_color(WHITE).scale(0.6)
                technique_3 = Text("- Feature Scaling").move_to([-2.5, -3.0, 0]).set_color(WHITE).scale(0.6)
                technique_4 = Text("- Handling Categorical Variables").move_to([-2.5, -3.5, 0]).set_color(WHITE).scale(0.6)
                impact_text = Text("Good features enhance model quality.").move_to([3.0, -2.75, 0]).set_color(GREEN).scale(0.8)
                domain_knowledge_text = Text("Domain knowledge is crucial.").move_to([0, -4.5, 0]).set_color(RED).scale(0.9)

                # Animation Timeline
                # start_time: 0.0, animation_id: anim_part_title, duration: 1.0
                self.play(FadeIn(part_series_text, title_text), run_time=1.0)

                # start_time: 1.0, animation_id: anim_definition_1, duration: 2.0
                self.play(Write(definition_text_1), run_time=2.0)

                # start_time: 3.0, animation_id: anim_definition_2, duration: 1.5
                self.play(Write(definition_text_2), run_time=1.5)

                # start_time: 4.5, animation_id: anim_techniques_title, duration: 1.0
                self.play(Write(techniques_title), run_time=1.0)

                # start_time: 5.5, animation_id: anim_technique_1, duration: 0.8
                self.play(Write(technique_1), run_time=0.8)

                # start_time: 6.3, animation_id: anim_technique_2, duration: 0.8
                self.play(Write(technique_2), run_time=0.8)

                # start_time: 7.1, animation_id: anim_technique_3, duration: 0.8
                self.play(Write(technique_3), run_time=0.8)

                # start_time: 7.9, animation_id: anim_technique_4, duration: 1.0
                self.play(Write(technique_4), run_time=1.0)

                # start_time: 8.9, animation_id: anim_impact, duration: 1.5
                self.play(Write(impact_text), run_time=1.5)

                # start_time: 10.4, animation_id: anim_domain_knowledge, duration: 1.2
                self.play(Write(domain_knowledge_text), run_time=1.2)

                # Current time after last animation: 10.4 + 1.2 = 11.6s
                self.wait(12.0 - 11.6)
        
        # Scene transition
        self.wait(0.5)