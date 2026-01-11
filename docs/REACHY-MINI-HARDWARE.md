# Reachy Mini Hardware Capabilities

**Last Updated**: January 10, 2026  
**Source**: [Pollen Robotics Official Site](https://www.pollen-robotics.com/reachy-mini/) & [GitHub SDK](https://github.com/pollen-robotics/reachy_mini)

---

## 🤖 What Reachy Mini IS

**Reachy Mini** is an open-source desktop robot ($299-$449) designed for:
- Human-robot interaction experiments
- Voice-based AI assistants
- Creative custom applications
- Educational robotics

**Key Characteristic**: Expressive, compact, **desktop-sized** robot (not a full humanoid)

---

## ✅ Actual Physical Capabilities

### Head Movement
- **6 degrees of freedom (DoF) head movement**
  - Pitch (up/down)
  - Yaw (left/right)
  - Roll (tilt side to side)
  - X, Y, Z positional movement
- **Example**: Can look up, nod, turn to face people, tilt expressively

### Body
- **Full 360° body rotation** - Can spin to face any direction
- **NO ARMS** - Reachy Mini is a head-and-body robot, not humanoid with limbs

### Antennas
- **2 animated antennas** on top of head (motorized, 1 DoF rotation each)
- Physical expressive appendages (not LED displays)
- Used for:
  - Emotional expression through movement (wiggle, tilt, bounce)
  - Status indicators via motion patterns
  - Engagement cues through animated gestures

### Sensors & I/O
- **Wide-angle camera** (front-facing)
- **4 microphones** (for voice input, sound localization)
- **5W speaker** (TTS output)
- **Accelerometer** (Wireless version only) - detects movement, tilt, bumps

### Compute
- **Reachy Mini Wireless**: Raspberry Pi 4 onboard (autonomous)
- **Reachy Mini Lite**: External compute (Mac/Linux via USB-C)

---

## ❌ What Reachy Mini CANNOT Do

### No Physical Manipulation
- ❌ **No arms** - Cannot point, wave, grab, or gesture with limbs
- ❌ **No hands** - Cannot hold objects
- ❌ **No manipulation** - Cannot move physical items

### Limited Mobility
- ❌ **No wheels or legs** - Stationary on desk/table
- ❌ **No navigation** - Cannot move around a space

### Physical Gestures
- ❌ Cannot physically point to aisles or products
- ❌ Cannot wave hands for greetings
- ✅ **Can express emotion through**:
  - Head movements (nodding, shaking, tilting)
  - Antenna animations (LED patterns, colors)
  - Body rotation (turning to face people)

---

## 🎯 Correct Use Cases for Retail Assistant

### ✅ What Works
1. **Voice Interaction**
   - Natural conversation via microphone + speaker
   - Product search, wayfinding, promotions

2. **Visual Engagement**
   - Camera for face detection, tracking customers
   - Screen-based visual aids (if connected to external display)

3. **Expressive Communication**
   - Head nods for confirmation ("Yes, aisle 5")
   - Head shake for negation ("Sorry, out of stock")
   - Antenna movements (wiggle = excited, perk up = listening, etc.)
   - Body rotation to "face" the customer

4. **Direction Indication**
   - **Verbal directions**: "The milk is in aisle 5 on your left"
   - **Head orientation**: Turn body/head toward the general direction
   - **Screen overlay**: Display map/arrow if using external screen

### ❌ What Doesn't Work
- Physical pointing with arms (REMOVE from docs)
- Waving goodbye with hands (REMOVE from docs)
- Grabbing products to show (REMOVE from docs)
- Leading customers physically (REMOVE from docs)

---

## 📊 Technical Specifications

| Feature | Reachy Mini Lite | Reachy Mini Wireless |
|---------|------------------|----------------------|
| **Price** | $299 + shipping | $449 + shipping |
| **Compute** | External (USB-C) | Raspberry Pi 4 onboard |
| **Power** | Wall outlet (wired) | Battery + wired/wireless |
| **WiFi** | No | Yes (or Ethernet adapter) |
| **Accelerometer** | No | Yes |
| **Head DoF** | 6 | 6 |
| **Body Rotation** | 360° | 360° |
| **Antennas** | 2 motorized (1 DoF each) | 2 motorized (1 DoF each) |
| **Microphones** | 4 | 4 |
| **Speaker** | 5W | 5W |
| **Camera** | Wide-angle | Wide-angle |

---

## 🔧 SDK Movement API

From Reachy Mini SDK documentation:

```python
from reachy_mini import ReachyMini
from reachy_mini.utils import create_head_pose

with ReachyMini() as mini:
    # Look up and tilt head
    mini.goto_target(
        head=create_head_pose(z=10, roll=15, degrees=True, mm=True),
        duration=1.0
    )
```

**Available Controls:**
- Head position (x, y, z in mm)
- Head orientation (pitch, yaw, roll in degrees)
- Duration for smooth movements
- Body rotation angle

---

## 💡 Revised Gesture Strategy for Retail

### Instead of Physical Pointing:
1. **Head Orientation** - Turn head/body toward the general direction
2. **Verbal Precision** - "Aisle 5 is behind me on your left"
3. **Visual Aids** - Display arrows on external screen/tablet if available
4. **Antenna Indicators** - Flash antennas in direction of product location

### Expressive Movements:
- **Nodding**: Confirmation, agreement
- **Head Shake**: Negation, "no"
- **Tilt**: Curiosity, confusion (for clarification prompts)
- **Body Spin**: Attention-getting, excitement about promotions
- **Antenna wiggle/bounce**: Excitement, acknowledgment, thinking

---

## 🎨 Antenna Expression Vocabulary

Antennas are motorized appendages that convey states through physical movement:

| State | Antenna Behavior |
|-------|------------------|
| **Idle** | Slight sway or rest position |
| **Listening** | Perk up/alert position |
| **Thinking** | Slow alternating tilt |
| **Speaking** | Gentle bounce/wiggle |
| **Error** | Droop or rapid shake |
| **Excited** (promo) | Rapid wiggle/bounce |
| **Directional hint** | Tilt toward product direction |

---

## 📝 Documentation Corrections Needed

### Files to Update:
1. ✅ This file (new reference doc)
2. ⚠️ `docs/PRD.md` - Remove arm pointing references
3. ⚠️ `reachy_edge/tools/movement.py` - Update to head/antenna only
4. ⚠️ `README.md` - Clarify gesture = head/antennas, not arms
5. ⚠️ Epic/Story files - Adjust expectations for gestures

### Key Changes:
- **REMOVE**: "arm pointing", "waving", "physical gestures with limbs"
- **ADD**: "head orientation", "antenna animations", "body rotation"
- **CLARIFY**: Gestures = expressive head movements + LED signals

---

## 🔗 Official Resources

- **Product Page**: https://www.pollen-robotics.com/reachy-mini/
- **GitHub SDK**: https://github.com/pollen-robotics/reachy_mini
- **Hugging Face Apps**: https://hf.co/reachy-mini
- **Discord Community**: https://discord.gg/2bAhWfXme9
- **Assembly Guide**: https://huggingface.co/spaces/pollen-robotics/Reachy_Mini

---

## ✅ Summary for Development

**Reachy Mini CAN:**
- Speak (TTS) and listen (STT)
- Nod, shake head, tilt expressively
- Rotate body 360°
- Animate antennas with wiggle/tilt/bounce movements
- Detect faces, track people with camera
- Process audio for voice commands

**Reachy Mini CANNOT:**
- Point with arms (doesn't have arms)
- Wave, grab, manipulate objects
- Move around space (stationary)
- Physically lead customers

**Design Principle**: Use **voice + head orientation + antenna movements** instead of physical pointing.
